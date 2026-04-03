#!/usr/bin/env python3
"""AWS infrastructure health metrics from existing inventory JSON. No API calls needed."""

import json
import os
import glob
from collections import defaultdict
from datetime import datetime, timezone

EOL_RUNTIMES = {
    'python2.7', 'python3.6', 'python3.7',
    'nodejs', 'nodejs4.3', 'nodejs6.10', 'nodejs8.10', 'nodejs10.x', 'nodejs12.x',
    'dotnetcore1.0', 'dotnetcore2.0', 'dotnetcore2.1', 'dotnetcore3.1',
    'ruby2.5',
    'java8',
}
PRE_GRAVITON = {'m1', 'm2', 'm3', 'm4', 'm5', 'm5a', 'c3', 'c4', 'c5', 'r3', 'r4', 'r5', 't2', 't3', 't3a'}


def load_all_accounts():
    accounts = {}
    for f in sorted(glob.glob('inventory/aws/mm-*.json')):
        with open(f) as fh:
            data = json.load(fh)
        profile = data.get('profile', os.path.basename(f).replace('.json', ''))
        accounts[profile] = data
    return accounts

def extract_costs(accounts):
    rows = []
    for profile, data in accounts.items():
        acct_id = data.get('account_id', '')
        cost_data = data.get('cost', {})
        if isinstance(cost_data, list):
            for period in cost_data:
                start = period.get('TimePeriod', {}).get('Start', '')
                for group in period.get('Groups', []):
                    service = group.get('Keys', [''])[0]
                    amount = float(group.get('Metrics', {}).get('UnblendedCost', {}).get('Amount', 0))
                    if amount > 0.01:
                        rows.append({
                            'profile': profile, 'account_id': acct_id,
                            'month': start, 'service': service,
                            'cost': round(amount, 2),
                        })
    return rows

def extract_resources(accounts):
    resources = []
    for profile, data in accounts.items():
        acct_id = data.get('account_id', '')
        for region, rdata in data.get('regions', {}).items():
            if isinstance(rdata, dict):
                for inst in rdata.get('ec2_instances', []):
                    if isinstance(inst, dict) and 'id' in inst:
                        inst_family = inst.get('type', '').split('.')[0] if inst.get('type') else ''
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'EC2', 'id': inst['id'],
                            'name': inst.get('name', ''), 'state': inst.get('state', ''),
                            'instance_type': inst.get('type', ''),
                            'is_graviton': inst_family.endswith('g') if inst_family else False,
                            'is_pre_graviton': inst_family in PRE_GRAVITON,
                        })
                for fn in rdata.get('lambda_functions', []):
                    if isinstance(fn, dict) and 'name' in fn:
                        runtime = fn.get('runtime', 'N/A')
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'Lambda', 'id': fn['name'], 'name': fn['name'],
                            'runtime': runtime,
                            'is_eol': runtime.lower().replace('.', '') in EOL_RUNTIMES or runtime in EOL_RUNTIMES,
                            'memory_mb': fn.get('memory', 0),
                            'last_modified': fn.get('last_modified', ''),
                        })
                for db in rdata.get('rds_instances', []):
                    if isinstance(db, dict) and 'id' in db:
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'RDS', 'id': db['id'], 'name': db['id'],
                            'engine': db.get('engine', ''), 'instance_class': db.get('class', ''),
                            'multi_az': db.get('multi_az', False),
                        })
                for stack in rdata.get('cloudformation_stacks', []):
                    if isinstance(stack, dict) and 'name' in stack:
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'CloudFormation', 'id': stack['name'], 'name': stack['name'],
                            'status': stack.get('status', ''), 'created': stack.get('created', ''),
                        })
                for cluster in rdata.get('eks_clusters', []):
                    if isinstance(cluster, str):
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'EKS', 'id': cluster, 'name': cluster,
                        })
                ecs_clusters = rdata.get('ecs_clusters', [])
                if isinstance(ecs_clusters, list):
                    for cluster in ecs_clusters:
                        if isinstance(cluster, str):
                            resources.append({
                                'profile': profile, 'account_id': acct_id, 'region': region,
                                'type': 'ECS', 'id': cluster.split('/')[-1],
                                'name': cluster.split('/')[-1],
                            })
                for bucket in rdata.get('s3_buckets', []):
                    if isinstance(bucket, dict) and 'name' in bucket:
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'S3', 'id': bucket['name'], 'name': bucket['name'],
                            'created': bucket.get('created', ''),
                        })
                for repo in rdata.get('ecr_repositories', []):
                    if isinstance(repo, str):
                        resources.append({
                            'profile': profile, 'account_id': acct_id, 'region': region,
                            'type': 'ECR', 'id': repo, 'name': repo,
                        })
    return resources

def compute_lambda_audit(resources):
    lambdas = [r for r in resources if r['type'] == 'Lambda']
    by_runtime = defaultdict(int)
    eol_count = 0
    for fn in lambdas:
        rt = fn.get('runtime', 'unknown')
        by_runtime[rt] += 1
        if fn.get('is_eol'):
            eol_count += 1
    return {
        'total_functions': len(lambdas),
        'eol_count': eol_count,
        'by_runtime': dict(sorted(by_runtime.items(), key=lambda x: -x[1])),
    }

def compute_instance_audit(resources):
    ec2s = [r for r in resources if r['type'] == 'EC2']
    running = [e for e in ec2s if e.get('state') == 'running']
    stopped = [e for e in ec2s if e.get('state') == 'stopped']
    pre_graviton = [e for e in running if e.get('is_pre_graviton')]
    return {
        'total_instances': len(ec2s),
        'running': len(running),
        'stopped': len(stopped),
        'pre_graviton_running': len(pre_graviton),
        'by_type': dict(sorted(
            defaultdict(int, {e.get('instance_type', '?'): 0 for e in running}).items()
        )),
    }

def compute_cost_summary(cost_rows):
    by_account = defaultdict(float)
    by_service = defaultdict(float)
    for r in cost_rows:
        if '2026-03' in r.get('month', ''):
            by_account[r['profile']] += r['cost']
            by_service[r['service']] += r['cost']
    return {
        'march_2026_by_account': dict(sorted(by_account.items(), key=lambda x: -x[1])),
        'march_2026_by_service': dict(sorted(by_service.items(), key=lambda x: -x[1])[:20]),
        'march_2026_total': round(sum(by_account.values()), 2),
    }


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    print("=== Loading AWS inventory data ===", flush=True)
    accounts = load_all_accounts()
    print(f"  Loaded {len(accounts)} accounts", flush=True)

    print("\n=== Extracting costs ===", flush=True)
    costs = extract_costs(accounts)
    print(f"  {len(costs)} cost line items", flush=True)
    with open('inventory/aws/cost_normalized.json', 'w') as f:
        json.dump(costs, f, indent=2)

    cost_summary = compute_cost_summary(costs)
    print(f"  March 2026 total: ${cost_summary['march_2026_total']:,.2f}", flush=True)
    with open('inventory/aws/cost_summary.json', 'w') as f:
        json.dump(cost_summary, f, indent=2)

    print("\n=== Extracting resources ===", flush=True)
    resources = extract_resources(accounts)
    print(f"  {len(resources)} total resources", flush=True)
    with open('inventory/aws/resources_flat.json', 'w') as f:
        json.dump(resources, f, indent=2)

    print("\n=== Lambda Runtime Audit ===", flush=True)
    lambda_audit = compute_lambda_audit(resources)
    print(f"  {lambda_audit['total_functions']} functions, {lambda_audit['eol_count']} on EOL runtimes", flush=True)
    with open('inventory/aws/lambda_audit.json', 'w') as f:
        json.dump(lambda_audit, f, indent=2)

    print("\n=== EC2 Instance Audit ===", flush=True)
    instance_audit = compute_instance_audit(resources)
    print(f"  {instance_audit['running']} running, {instance_audit['stopped']} stopped, "
          f"{instance_audit['pre_graviton_running']} pre-Graviton", flush=True)
    with open('inventory/aws/instance_audit.json', 'w') as f:
        json.dump(instance_audit, f, indent=2)

    print("\nDone.", flush=True)
