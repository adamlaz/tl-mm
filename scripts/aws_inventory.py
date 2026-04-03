#!/usr/bin/env python3
"""AWS account inventory via SSO profiles. Outputs JSON per account."""

import boto3
import json
import sys
import os
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError, NoCredentialsError

REGIONS_TO_CHECK = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]

def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess',
                     'AuthorizationError', 'OptInRequired', 'SubscriptionRequiredException'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}

def inventory_region(session, region):
    result = {}

    ec2 = session.client('ec2', region_name=region)
    result['ec2_instances'] = safe_call(
        lambda: [{'id': i['InstanceId'], 'type': i['InstanceType'], 'state': i['State']['Name'],
                   'name': next((t['Value'] for t in i.get('Tags', []) if t['Key'] == 'Name'), '')}
                  for r in ec2.describe_instances()['Reservations'] for i in r['Instances']], [])

    result['vpcs'] = safe_call(
        lambda: [{'id': v['VpcId'], 'cidr': v['CidrBlock'], 'default': v['IsDefault']}
                  for v in ec2.describe_vpcs()['Vpcs']], [])

    lam = session.client('lambda', region_name=region)
    result['lambda_functions'] = safe_call(
        lambda: [{'name': f['FunctionName'], 'runtime': f.get('Runtime', 'N/A'),
                   'memory': f.get('MemorySize'), 'last_modified': f.get('LastModified', '')}
                  for f in lam.list_functions()['Functions']], [])

    ecs = session.client('ecs', region_name=region)
    clusters = safe_call(lambda: ecs.list_clusters()['clusterArns'], [])
    result['ecs_clusters'] = clusters if isinstance(clusters, dict) and '_error' in clusters else clusters
    if isinstance(clusters, list) and clusters:
        result['ecs_services'] = safe_call(
            lambda: {c.split('/')[-1]: ecs.list_services(cluster=c)['serviceArns']
                     for c in clusters}, {})

    eks = session.client('eks', region_name=region)
    result['eks_clusters'] = safe_call(lambda: eks.list_clusters()['clusters'], [])

    rds = session.client('rds', region_name=region)
    result['rds_instances'] = safe_call(
        lambda: [{'id': db['DBInstanceIdentifier'], 'engine': db['Engine'],
                   'class': db['DBInstanceClass'], 'status': db['DBInstanceStatus'],
                   'multi_az': db.get('MultiAZ', False)}
                  for db in rds.describe_db_instances()['DBInstances']], [])

    ddb = session.client('dynamodb', region_name=region)
    result['dynamodb_tables'] = safe_call(lambda: ddb.list_tables()['TableNames'], [])

    s3_client = session.client('s3', region_name=region)
    if region == REGIONS_TO_CHECK[0]:
        result['s3_buckets'] = safe_call(
            lambda: [{'name': b['Name'], 'created': b['CreationDate'].isoformat()}
                      for b in s3_client.list_buckets()['Buckets']], [])

    cw = session.client('cloudwatch', region_name=region)
    result['cloudwatch_alarms'] = safe_call(
        lambda: len(cw.describe_alarms()['MetricAlarms']), 0)
    result['cloudwatch_dashboards'] = safe_call(
        lambda: [d['DashboardName'] for d in cw.list_dashboards()['DashboardEntries']], [])

    cfn = session.client('cloudformation', region_name=region)
    result['cloudformation_stacks'] = safe_call(
        lambda: [{'name': s['StackName'], 'status': s['StackStatus'],
                   'created': s['CreationTime'].isoformat()}
                  for s in cfn.describe_stacks()['Stacks']], [])

    sns = session.client('sns', region_name=region)
    result['sns_topics'] = safe_call(lambda: len(sns.list_topics()['Topics']), 0)

    sqs = session.client('sqs', region_name=region)
    result['sqs_queues'] = safe_call(lambda: len(sqs.list_queues().get('QueueUrls', [])), 0)

    ecr = session.client('ecr', region_name=region)
    result['ecr_repositories'] = safe_call(
        lambda: [r['repositoryName'] for r in ecr.describe_repositories()['repositories']], [])

    sm = session.client('secretsmanager', region_name=region)
    result['secrets_count'] = safe_call(
        lambda: len(list(sm.get_paginator('list_secrets').paginate())), 0)

    return result

def inventory_global(session):
    result = {}

    iam = session.client('iam', region_name='us-east-1')
    result['iam_users'] = safe_call(lambda: len(iam.list_users()['Users']), 0)
    result['iam_roles'] = safe_call(lambda: len(iam.list_roles()['Roles']), 0)
    result['iam_policies'] = safe_call(
        lambda: len(iam.list_policies(Scope='Local')['Policies']), 0)

    orgs = session.client('organizations', region_name='us-east-1')
    result['organization'] = safe_call(
        lambda: {'id': orgs.describe_organization()['Organization']['Id']})

    return result

def inventory_cost(session):
    ce = session.client('ce', region_name='us-east-1')
    end = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    start = (datetime.now(timezone.utc) - timedelta(days=90)).strftime('%Y-%m-%d')
    return safe_call(lambda: ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )['ResultsByTime'])


def run(profile_name):
    session = boto3.Session(profile_name=profile_name)
    sts = session.client('sts')
    identity = sts.get_caller_identity()

    result = {
        'profile': profile_name,
        'account_id': identity['Account'],
        'arn': identity['Arn'],
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'regions': {},
        'global': {},
        'cost': {},
    }

    result['global'] = inventory_global(session)

    for region in REGIONS_TO_CHECK:
        print(f"  Scanning {region}...", flush=True)
        result['regions'][region] = inventory_region(session, region)

    print(f"  Checking cost explorer...", flush=True)
    result['cost'] = inventory_cost(session)

    return result


if __name__ == '__main__':
    profiles = sys.argv[1:]
    if not profiles:
        print("Usage: aws_inventory.py <profile1> [profile2] ...")
        sys.exit(1)

    os.makedirs('inventory/aws', exist_ok=True)
    for profile in profiles:
        print(f"\n=== Inventorying {profile} ===", flush=True)
        try:
            data = run(profile)
            outfile = f"inventory/aws/{profile}.json"
            with open(outfile, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"  -> Wrote {outfile}")
        except (NoCredentialsError, ClientError) as e:
            print(f"  ERROR on {profile}: {e}")
            with open(f"inventory/aws/{profile}.json", 'w') as f:
                json.dump({"profile": profile, "error": str(e)}, f, indent=2)
