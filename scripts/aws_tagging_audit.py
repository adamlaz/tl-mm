#!/usr/bin/env python3
"""Tagging compliance audit from local AWS inventory JSON files.

Reads inventory/aws/mm-*.json files. Since raw AWS tags weren't captured in the
inventory collection, this script audits *naming conventions* as a proxy for
organizational hygiene:
  - EC2: checks if instance names follow env-service or team-env-service patterns
  - Lambda: checks for team/project prefix patterns in function names
  - S3: checks for organizational naming patterns in bucket names
  - All: flags resources with missing or generic names
"""

import json
import os
import re
import glob
from collections import defaultdict
from datetime import datetime

os.makedirs('inventory/aws', exist_ok=True)

KNOWN_ENVS = {'prod', 'staging', 'stg', 'dev', 'development', 'test', 'qa', 'uat', 'sandbox', 'dr', 'rnd'}
KNOWN_TEAMS = {'cake', 'retail', 'concierge', 'phoenix', 'payments', 'analytics', 'platform', 'ops',
               'mira', 'leo', 'castor', 'nova', 'apollo', 'vega', 'drac', 'thor', 'hulk',
               'taur', 'libra', 'pollux', 'maui', 'kenworth', 'wolverine'}
KNOWN_SERVICES = {'api', 'web', 'worker', 'scheduler', 'cron', 'proxy', 'bastion', 'vpn',
                  'elasticsearch', 'redis', 'rabbitmq', 'mongodb', 'postgres', 'mysql',
                  'prometheus', 'grafana', 'jenkins', 'deploy', 'support', 'node'}
AWS_MANAGED_PREFIXES = {'aws-controltower', 'aws-', 'AWSControlTower', 'StackSet-'}
GENERIC_NAMES = {'', 'default', 'test', 'temp', 'tmp', 'untitled'}


def load_all_accounts():
    accounts = {}
    for f in sorted(glob.glob('inventory/aws/mm-*.json')):
        with open(f) as fh:
            data = json.load(fh)
        profile = data.get('profile', os.path.basename(f).replace('.json', ''))
        accounts[profile] = data
    return accounts


def extract_name_parts(name):
    """Split a resource name into tokens for pattern analysis."""
    return set(re.split(r'[-_./\s]+', name.lower()))


def check_ec2_naming(instance):
    """Evaluate EC2 naming compliance. Returns a dict of checks."""
    name = instance.get('name', '') or ''
    parts = extract_name_parts(name)

    has_env = bool(parts & KNOWN_ENVS)
    has_team = bool(parts & KNOWN_TEAMS)
    has_service = bool(parts & KNOWN_SERVICES)
    is_unnamed = name.strip() == '' or name.lower() in GENERIC_NAMES
    is_numbered = bool(re.search(r'\d{2}$', name))

    compliant_checks = 0
    total_checks = 4
    if has_env:
        compliant_checks += 1
    if has_team or has_service:
        compliant_checks += 1
    if not is_unnamed:
        compliant_checks += 1
    if is_numbered or has_service:
        compliant_checks += 1

    return {
        'name': name,
        'id': instance.get('id', ''),
        'type': instance.get('type', ''),
        'state': instance.get('state', ''),
        'has_environment_indicator': has_env,
        'has_team_or_service': has_team or has_service,
        'is_unnamed': is_unnamed,
        'compliance_score': compliant_checks / total_checks,
        'issues': [
            *(["no_environment_in_name"] if not has_env else []),
            *(["no_team_or_service_in_name"] if not (has_team or has_service) else []),
            *(["unnamed_or_generic"] if is_unnamed else []),
        ],
    }


def check_lambda_naming(fn):
    """Evaluate Lambda naming compliance."""
    name = fn.get('name', '') or ''
    parts = extract_name_parts(name)
    is_aws_managed = any(name.startswith(p) for p in AWS_MANAGED_PREFIXES)

    has_env = bool(parts & KNOWN_ENVS)
    has_team = bool(parts & KNOWN_TEAMS)
    has_prefix = bool(re.match(r'^[a-z]+-[a-z]+-', name))
    is_unnamed = name.strip() == ''

    if is_aws_managed:
        return {
            'name': name,
            'runtime': fn.get('runtime', ''),
            'aws_managed': True,
            'compliance_score': 1.0,
            'issues': [],
        }

    compliant_checks = 0
    total_checks = 3
    if has_prefix or has_team:
        compliant_checks += 1
    if has_env or has_team:
        compliant_checks += 1
    if not is_unnamed:
        compliant_checks += 1

    return {
        'name': name,
        'runtime': fn.get('runtime', ''),
        'last_modified': fn.get('last_modified', ''),
        'aws_managed': False,
        'has_structured_prefix': has_prefix,
        'has_team_indicator': has_team,
        'has_environment_indicator': has_env,
        'compliance_score': compliant_checks / total_checks,
        'issues': [
            *(["no_structured_prefix"] if not (has_prefix or has_team) else []),
            *(["no_environment_indicator"] if not has_env else []),
            *(["unnamed"] if is_unnamed else []),
        ],
    }


def check_s3_naming(bucket):
    """Evaluate S3 bucket naming compliance."""
    name = bucket.get('name', '') or ''
    parts = extract_name_parts(name)

    has_env = bool(parts & KNOWN_ENVS)
    has_team = bool(parts & KNOWN_TEAMS)
    has_org_prefix = name.startswith(('mm-', 'madmobile-', 'cake-', 'retail-', 'concierge-'))
    has_account_id = bool(re.search(r'\d{12}', name))
    is_aws_generated = name.startswith(('aws-', 'cf-templates-', 'cdk-', 'elasticbeanstalk-'))
    has_structured_name = bool(re.match(r'^[a-z]+-[a-z]+-[a-z]+', name))

    if is_aws_generated:
        return {
            'name': name,
            'created': bucket.get('created', ''),
            'aws_generated': True,
            'compliance_score': 1.0,
            'issues': [],
        }

    compliant_checks = 0
    total_checks = 3
    if has_org_prefix or has_team:
        compliant_checks += 1
    if has_env or has_account_id:
        compliant_checks += 1
    if has_structured_name:
        compliant_checks += 1

    return {
        'name': name,
        'created': bucket.get('created', ''),
        'aws_generated': False,
        'has_org_prefix': has_org_prefix,
        'has_environment_indicator': has_env,
        'has_structured_name': has_structured_name,
        'compliance_score': compliant_checks / total_checks,
        'issues': [
            *(["no_org_prefix"] if not (has_org_prefix or has_team) else []),
            *(["no_environment_indicator"] if not (has_env or has_account_id) else []),
            *(["unstructured_name"] if not has_structured_name else []),
        ],
    }


def main():
    print("=" * 60)
    print("AWS Tagging & Naming Compliance Audit")
    print("=" * 60)

    accounts = load_all_accounts()
    print(f"Loaded {len(accounts)} account inventory files\n")

    per_account = {}
    all_ec2 = []
    all_lambda = []
    all_s3 = []
    flagged_untagged = []

    for profile, data in sorted(accounts.items()):
        account_id = data.get('account_id', '')
        ec2_results = []
        lambda_results = []
        s3_results = []

        for region, rdata in data.get('regions', {}).items():
            if not isinstance(rdata, dict):
                continue

            for inst in rdata.get('ec2_instances', []):
                if isinstance(inst, dict) and 'id' in inst:
                    result = check_ec2_naming(inst)
                    result['profile'] = profile
                    result['region'] = region
                    ec2_results.append(result)
                    if result['is_unnamed']:
                        flagged_untagged.append({
                            'resource_type': 'EC2',
                            'id': inst['id'],
                            'profile': profile,
                            'region': region,
                            'reason': 'unnamed_or_generic',
                        })

            for fn in rdata.get('lambda_functions', []):
                if isinstance(fn, dict) and 'name' in fn:
                    result = check_lambda_naming(fn)
                    result['profile'] = profile
                    result['region'] = region
                    lambda_results.append(result)

            for bucket in rdata.get('s3_buckets', []):
                if isinstance(bucket, dict) and 'name' in bucket:
                    result = check_s3_naming(bucket)
                    result['profile'] = profile
                    result['region'] = region
                    s3_results.append(result)

        ec2_scores = [r['compliance_score'] for r in ec2_results]
        lambda_non_aws = [r for r in lambda_results if not r.get('aws_managed')]
        lambda_scores = [r['compliance_score'] for r in lambda_non_aws]
        s3_non_aws = [r for r in s3_results if not r.get('aws_generated')]
        s3_scores = [r['compliance_score'] for r in s3_non_aws]

        def avg(lst):
            return round(sum(lst) / len(lst) * 100, 1) if lst else None

        per_account[profile] = {
            'account_id': account_id,
            'ec2': {
                'total': len(ec2_results),
                'compliance_pct': avg(ec2_scores),
                'unnamed': sum(1 for r in ec2_results if r['is_unnamed']),
                'fully_compliant': sum(1 for r in ec2_results if r['compliance_score'] == 1.0),
            },
            'lambda': {
                'total': len(lambda_results),
                'aws_managed': len(lambda_results) - len(lambda_non_aws),
                'custom': len(lambda_non_aws),
                'compliance_pct': avg(lambda_scores),
                'fully_compliant': sum(1 for r in lambda_non_aws if r['compliance_score'] == 1.0),
            },
            's3': {
                'total': len(s3_results),
                'aws_generated': len(s3_results) - len(s3_non_aws),
                'custom': len(s3_non_aws),
                'compliance_pct': avg(s3_scores),
                'fully_compliant': sum(1 for r in s3_non_aws if r['compliance_score'] == 1.0),
            },
        }

        all_ec2.extend(ec2_results)
        all_lambda.extend(lambda_results)
        all_s3.extend(s3_results)

    ec2_all_scores = [r['compliance_score'] for r in all_ec2]
    lambda_custom = [r for r in all_lambda if not r.get('aws_managed')]
    lambda_all_scores = [r['compliance_score'] for r in lambda_custom]
    s3_custom = [r for r in all_s3 if not r.get('aws_generated')]
    s3_all_scores = [r['compliance_score'] for r in s3_custom]

    def avg(lst):
        return round(sum(lst) / len(lst) * 100, 1) if lst else None

    ec2_issues = defaultdict(int)
    for r in all_ec2:
        for issue in r.get('issues', []):
            ec2_issues[issue] += 1

    lambda_issues = defaultdict(int)
    for r in lambda_custom:
        for issue in r.get('issues', []):
            lambda_issues[issue] += 1

    s3_issues = defaultdict(int)
    for r in s3_custom:
        for issue in r.get('issues', []):
            s3_issues[issue] += 1

    output = {
        "extracted_at": datetime.now().isoformat(),
        "methodology": (
            "Tag data was not captured in inventory collection. This audit uses resource "
            "naming conventions as a proxy for organizational hygiene. Checks include: "
            "environment indicators, team/service identifiers, structured naming prefixes, "
            "and flagging unnamed/generic resources."
        ),
        "overall_summary": {
            "total_accounts": len(accounts),
            "ec2": {
                "total": len(all_ec2),
                "naming_compliance_pct": avg(ec2_all_scores),
                "unnamed": sum(1 for r in all_ec2 if r.get('is_unnamed')),
                "common_issues": dict(sorted(ec2_issues.items(), key=lambda x: -x[1])),
            },
            "lambda": {
                "total": len(all_lambda),
                "custom": len(lambda_custom),
                "aws_managed": len(all_lambda) - len(lambda_custom),
                "naming_compliance_pct": avg(lambda_all_scores),
                "common_issues": dict(sorted(lambda_issues.items(), key=lambda x: -x[1])),
            },
            "s3": {
                "total": len(all_s3),
                "custom": len(s3_custom),
                "aws_generated": len(all_s3) - len(s3_custom),
                "naming_compliance_pct": avg(s3_all_scores),
                "common_issues": dict(sorted(s3_issues.items(), key=lambda x: -x[1])),
            },
        },
        "per_account": per_account,
        "flagged_untagged_resources": flagged_untagged,
        "low_compliance_ec2": sorted(
            [r for r in all_ec2 if r['compliance_score'] < 0.5],
            key=lambda x: x['compliance_score'],
        ),
        "low_compliance_lambda": sorted(
            [r for r in lambda_custom if r['compliance_score'] < 0.34],
            key=lambda x: x['compliance_score'],
        ),
        "low_compliance_s3": sorted(
            [r for r in s3_custom if r['compliance_score'] < 0.34],
            key=lambda x: x['compliance_score'],
        ),
    }

    out_path = 'inventory/aws/tagging_compliance.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Wrote {out_path}")

    print("\n" + "=" * 60)
    print("OVERALL COMPLIANCE SUMMARY")
    print("=" * 60)

    print(f"\nEC2 Instances ({len(all_ec2)} total):")
    print(f"  Naming compliance: {avg(ec2_all_scores) or 0}%")
    print(f"  Unnamed/generic:   {sum(1 for r in all_ec2 if r.get('is_unnamed'))}")
    if ec2_issues:
        for issue, count in sorted(ec2_issues.items(), key=lambda x: -x[1]):
            print(f"    {issue}: {count}")

    print(f"\nLambda Functions ({len(all_lambda)} total, {len(lambda_custom)} custom):")
    print(f"  Naming compliance: {avg(lambda_all_scores) or 0}%")
    if lambda_issues:
        for issue, count in sorted(lambda_issues.items(), key=lambda x: -x[1]):
            print(f"    {issue}: {count}")

    print(f"\nS3 Buckets ({len(all_s3)} total, {len(s3_custom)} custom):")
    print(f"  Naming compliance: {avg(s3_all_scores) or 0}%")
    if s3_issues:
        for issue, count in sorted(s3_issues.items(), key=lambda x: -x[1]):
            print(f"    {issue}: {count}")

    print(f"\nPer-account breakdown:")
    for profile, stats in sorted(per_account.items()):
        ec2_pct = stats['ec2']['compliance_pct']
        lam_pct = stats['lambda']['compliance_pct']
        s3_pct = stats['s3']['compliance_pct']
        ec2_str = f"{ec2_pct}%" if ec2_pct is not None else "n/a"
        lam_str = f"{lam_pct}%" if lam_pct is not None else "n/a"
        s3_str = f"{s3_pct}%" if s3_pct is not None else "n/a"
        print(f"  {profile:35s}  EC2:{ec2_str:>6s}  Lambda:{lam_str:>6s}  S3:{s3_str:>6s}")

    if flagged_untagged:
        print(f"\nCompletely unnamed resources ({len(flagged_untagged)}):")
        for r in flagged_untagged[:20]:
            print(f"  [{r['resource_type']}] {r['id']} in {r['profile']}/{r['region']}")
        if len(flagged_untagged) > 20:
            print(f"  ... and {len(flagged_untagged) - 20} more")
    print()


if __name__ == '__main__':
    main()
