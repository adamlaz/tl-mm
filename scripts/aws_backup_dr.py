#!/usr/bin/env python3
"""AWS Backup and DR assessment — backup plans, vaults, RDS snapshots, S3 replication."""

import boto3
import json
import os
import glob
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess',
                     'AuthorizationError', 'OptInRequired', 'SubscriptionRequiredException',
                     'UnrecognizedClientException'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}

ACCOUNTS = [
    'mm-retail-prod-us',
    'mm-payments-prod-us',
    'mm-cake-development',
]

REGION = 'us-east-1'

KEY_BUCKETS = {
    'mm-retail-prod-us': [
        '07-11-2024-omni-backup',
        'analytics-accounting-reports',
        'bitbucket-oidc-prod-us-state-bucket',
    ],
    'mm-payments-prod-us': [
        'pay-eks-backend-mimir',
        'tf-payments-prod-us-state',
        'pay-elb-access-logs-east2',
    ],
    'mm-cake-development': [
        'ach-instructions',
        'archived-ach-instructions',
        'apig-dp-artifact',
    ],
}


def load_bucket_names_from_inventory(profile):
    """Load all bucket names from inventory for fallback."""
    for f in glob.glob('inventory/aws/mm-*.json'):
        with open(f) as fh:
            data = json.load(fh)
        if data.get('profile', '') == profile:
            for region, rdata in data.get('regions', {}).items():
                if isinstance(rdata, dict):
                    buckets = rdata.get('s3_buckets', [])
                    return [b['name'] for b in buckets if isinstance(b, dict) and 'name' in b]
    return []


def scan_backup_plans(session):
    backup = session.client('backup', region_name=REGION)
    raw = safe_call(lambda: backup.list_backup_plans().get('BackupPlansList', []), [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw

    plans = []
    for p in raw:
        plan_id = p.get('BackupPlanId', '')
        detail = safe_call(lambda pid=plan_id: backup.get_backup_plan(BackupPlanId=pid).get('BackupPlan', {}))
        rules = []
        if isinstance(detail, dict) and '_error' not in detail:
            for r in detail.get('Rules', []):
                rules.append({
                    'name': r.get('RuleName', ''),
                    'schedule': r.get('ScheduleExpression', ''),
                    'lifecycle_delete_days': r.get('Lifecycle', {}).get('DeleteAfterDays', 'N/A'),
                    'target_vault': r.get('TargetBackupVaultName', ''),
                })
        plans.append({
            'id': plan_id,
            'name': p.get('BackupPlanName', ''),
            'version': p.get('VersionId', ''),
            'created': p.get('CreationDate', ''),
            'last_execution': p.get('LastExecutionDate', ''),
            'rules': rules,
        })
    return plans


def scan_backup_vaults(session):
    backup = session.client('backup', region_name=REGION)
    raw = safe_call(lambda: backup.list_backup_vaults().get('BackupVaultList', []), [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw

    vaults = []
    for v in raw:
        vault_name = v.get('BackupVaultName', '')
        recovery_points = safe_call(
            lambda vn=vault_name: backup.list_recovery_points_by_backup_vault(
                BackupVaultName=vn, MaxResults=1
            ).get('RecoveryPoints', []), []
        )
        latest_rp = None
        if isinstance(recovery_points, list) and recovery_points:
            rp = recovery_points[0]
            latest_rp = {
                'arn': rp.get('RecoveryPointArn', ''),
                'status': rp.get('Status', ''),
                'created': rp.get('CreationDate', ''),
            }
        vaults.append({
            'name': vault_name,
            'recovery_points': v.get('NumberOfRecoveryPoints', 0),
            'encrypted': v.get('Locked', False),
            'created': v.get('CreationDate', ''),
            'latest_recovery_point': latest_rp,
        })
    return vaults


def scan_rds_snapshots(session):
    rds = session.client('rds', region_name=REGION)

    auto_raw = safe_call(lambda: rds.describe_db_snapshots(
        SnapshotType='automated', MaxRecords=100
    ).get('DBSnapshots', []), [])

    manual_raw = safe_call(lambda: rds.describe_db_snapshots(
        SnapshotType='manual', MaxRecords=100
    ).get('DBSnapshots', []), [])

    if isinstance(auto_raw, dict) and '_error' in auto_raw:
        return auto_raw
    if isinstance(manual_raw, dict) and '_error' in manual_raw:
        return manual_raw

    auto_dates = []
    for s in auto_raw:
        created = s.get('SnapshotCreateTime')
        if created:
            auto_dates.append(created)

    manual_dates = []
    for s in manual_raw:
        created = s.get('SnapshotCreateTime')
        if created:
            manual_dates.append(created)

    most_recent_auto = max(auto_dates).isoformat() if auto_dates else 'none'
    most_recent_manual = max(manual_dates).isoformat() if manual_dates else 'none'

    auto_by_db = {}
    for s in auto_raw:
        db_id = s.get('DBInstanceIdentifier', 'unknown')
        auto_by_db[db_id] = auto_by_db.get(db_id, 0) + 1

    return {
        'automated_count': len(auto_raw),
        'manual_count': len(manual_raw),
        'most_recent_automated': most_recent_auto,
        'most_recent_manual': most_recent_manual,
        'automated_by_db': auto_by_db,
    }


def scan_s3_replication(session, profile):
    s3 = session.client('s3', region_name=REGION)
    buckets_to_check = KEY_BUCKETS.get(profile, [])
    results = []

    for bucket_name in buckets_to_check:
        replication = safe_call(
            lambda bn=bucket_name: s3.get_bucket_replication(Bucket=bn).get('ReplicationConfiguration', {}),
            None
        )
        versioning = safe_call(
            lambda bn=bucket_name: s3.get_bucket_versioning(Bucket=bn),
            {}
        )
        ver_status = 'unknown'
        if isinstance(versioning, dict) and '_error' not in versioning:
            ver_status = versioning.get('Status', 'Disabled')

        if replication is None:
            results.append({
                'bucket': bucket_name,
                'replication_enabled': False,
                'versioning': ver_status,
                'rules': [],
            })
        elif isinstance(replication, dict) and '_error' in replication:
            results.append({
                'bucket': bucket_name,
                'replication_enabled': False,
                'versioning': ver_status,
                '_note': replication['_error'],
            })
        else:
            rules = []
            for r in replication.get('Rules', []):
                dest = r.get('Destination', {})
                rules.append({
                    'id': r.get('ID', ''),
                    'status': r.get('Status', ''),
                    'dest_bucket': dest.get('Bucket', '').split(':')[-1] if dest.get('Bucket') else '',
                    'storage_class': dest.get('StorageClass', 'STANDARD'),
                })
            results.append({
                'bucket': bucket_name,
                'replication_enabled': True,
                'versioning': ver_status,
                'rules': rules,
            })

    return results


def scan_account(profile):
    print(f"\n  [{profile}]", flush=True)
    session = boto3.Session(profile_name=profile)
    data = {'profile': profile}
    blocked = []

    print(f"    Backup Plans ...", end='', flush=True)
    plans = scan_backup_plans(session)
    data['backup_plans'] = plans
    if isinstance(plans, dict) and '_error' in plans:
        blocked.append(f"Backup Plans: {plans['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {len(plans)} plans", flush=True)
        for p in plans:
            print(f"      {p['name']} ({len(p.get('rules', []))} rules)", flush=True)

    print(f"    Backup Vaults ...", end='', flush=True)
    vaults = scan_backup_vaults(session)
    data['backup_vaults'] = vaults
    if isinstance(vaults, dict) and '_error' in vaults:
        blocked.append(f"Backup Vaults: {vaults['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        total_rps = sum(v.get('recovery_points', 0) for v in vaults)
        print(f" {len(vaults)} vaults, {total_rps} recovery points", flush=True)

    print(f"    RDS Snapshots ...", end='', flush=True)
    snapshots = scan_rds_snapshots(session)
    data['rds_snapshots'] = snapshots
    if isinstance(snapshots, dict) and '_error' in snapshots:
        blocked.append(f"RDS Snapshots: {snapshots['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {snapshots.get('automated_count', 0)} automated, {snapshots.get('manual_count', 0)} manual", flush=True)
        print(f"      Most recent auto: {snapshots.get('most_recent_automated', 'N/A')}", flush=True)
        print(f"      Most recent manual: {snapshots.get('most_recent_manual', 'N/A')}", flush=True)

    print(f"    S3 Replication ...", end='', flush=True)
    replication = scan_s3_replication(session, profile)
    data['s3_replication'] = replication
    replicated = [r for r in replication if r.get('replication_enabled')]
    print(f" {len(replicated)}/{len(replication)} key buckets have replication", flush=True)
    for r in replication:
        status = "✓ replicated" if r.get('replication_enabled') else "✗ no replication"
        print(f"      {r['bucket']}: {status} (versioning: {r.get('versioning', '?')})", flush=True)

    data['blocked_apis'] = blocked
    return data


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    print("=== AWS Backup & DR Assessment ===", flush=True)
    print(f"  Accounts: {len(ACCOUNTS)}", flush=True)
    print(f"  Region: {REGION}", flush=True)
    print(f"  Started: {datetime.now(timezone.utc).isoformat()}", flush=True)

    results = {}
    for profile in ACCOUNTS:
        results[profile] = scan_account(profile)

    output = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'region': REGION,
        'accounts_scanned': len(ACCOUNTS),
        'accounts': results,
    }

    outpath = 'inventory/aws/backup_dr.json'
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Wrote {outpath}", flush=True)

    print("\n=== DR Readiness Summary ===", flush=True)
    for profile, data in results.items():
        blocked = data.get('blocked_apis', [])
        print(f"\n  {profile}:", flush=True)
        if blocked:
            print(f"    Blocked: {', '.join(blocked)}", flush=True)

        plans = data.get('backup_plans', [])
        if isinstance(plans, list):
            print(f"    Backup Plans: {len(plans)}", flush=True)

        vaults = data.get('backup_vaults', [])
        if isinstance(vaults, list):
            total_rps = sum(v.get('recovery_points', 0) for v in vaults)
            print(f"    Backup Vaults: {len(vaults)} ({total_rps} recovery points)", flush=True)

        snaps = data.get('rds_snapshots', {})
        if isinstance(snaps, dict) and '_error' not in snaps:
            print(f"    RDS Snapshots: {snaps.get('automated_count',0)} auto / {snaps.get('manual_count',0)} manual", flush=True)
            print(f"      Latest auto: {snaps.get('most_recent_automated','N/A')}", flush=True)

        repl = data.get('s3_replication', [])
        if isinstance(repl, list):
            yes = sum(1 for r in repl if r.get('replication_enabled'))
            print(f"    S3 Replication: {yes}/{len(repl)} key buckets replicated", flush=True)

    print("\nDone.", flush=True)
