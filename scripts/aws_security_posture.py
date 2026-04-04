#!/usr/bin/env python3
"""AWS security posture deep scan across production accounts."""

import boto3
import json
import os
import base64
import csv
import io
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
    'mm-cake-r-and-d',
    'mm-shared-services',
    'mm-security',
    'mm-madmobile-mgmt',
]

REGION = 'us-east-1'


def scan_guardduty(session):
    gd = session.client('guardduty', region_name=REGION)
    detectors = safe_call(lambda: gd.list_detectors()['DetectorIds'], [])
    if isinstance(detectors, dict) and '_error' in detectors:
        return detectors

    results = {'detectors': [], 'finding_stats': {}}
    for det_id in detectors:
        status = safe_call(lambda: gd.get_detector(DetectorId=det_id))
        if isinstance(status, dict) and '_error' not in status:
            results['detectors'].append({
                'id': det_id,
                'status': status.get('Status', 'unknown'),
                'updated_at': status.get('UpdatedAt', ''),
            })
        stats = safe_call(lambda: gd.get_finding_statistics(
            DetectorId=det_id,
            FindingStatisticTypes=['COUNT_BY_SEVERITY']
        ))
        if isinstance(stats, dict) and '_error' not in stats:
            count_by_sev = stats.get('FindingStatistics', {}).get('CountBySeverity', {})
            results['finding_stats'] = {str(k): v for k, v in count_by_sev.items()}

    if not detectors:
        results['_note'] = 'No GuardDuty detectors found'
    return results


def scan_acm(session):
    acm = session.client('acm', region_name=REGION)
    raw = safe_call(lambda: acm.list_certificates(
        CertificateStatuses=['ISSUED', 'PENDING_VALIDATION', 'EXPIRED', 'INACTIVE', 'FAILED']
    ).get('CertificateSummaryList', []), [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw

    certs = []
    for c in raw:
        detail = safe_call(lambda: acm.describe_certificate(
            CertificateArn=c['CertificateArn']
        ).get('Certificate', {}))
        if isinstance(detail, dict) and '_error' not in detail:
            not_after = detail.get('NotAfter')
            certs.append({
                'domain': detail.get('DomainName', ''),
                'status': detail.get('Status', ''),
                'type': detail.get('Type', ''),
                'renewal_status': detail.get('RenewalSummary', {}).get('RenewalStatus', 'N/A'),
                'not_after': not_after.isoformat() if hasattr(not_after, 'isoformat') else str(not_after or ''),
                'in_use': bool(detail.get('InUseBy')),
            })
    return {'total': len(certs), 'certificates': certs}


def scan_iam(session):
    iam = session.client('iam')
    result = {}

    summary = safe_call(lambda: iam.get_account_summary()['SummaryMap'])
    if isinstance(summary, dict) and '_error' not in summary:
        result['account_summary'] = {
            'users': summary.get('Users', 0),
            'groups': summary.get('Groups', 0),
            'roles': summary.get('Roles', 0),
            'policies': summary.get('Policies', 0),
            'mfa_devices': summary.get('MFADevicesInUse', 0),
            'access_keys_active': summary.get('AccessKeysPerUserQuota', 0),
        }

    pw_policy = safe_call(lambda: iam.get_account_password_policy()['PasswordPolicy'])
    if isinstance(pw_policy, dict) and '_error' not in pw_policy:
        result['password_policy'] = {
            'min_length': pw_policy.get('MinimumPasswordLength', 0),
            'require_uppercase': pw_policy.get('RequireUppercaseCharacters', False),
            'require_lowercase': pw_policy.get('RequireLowercaseCharacters', False),
            'require_numbers': pw_policy.get('RequireNumbers', False),
            'require_symbols': pw_policy.get('RequireSymbols', False),
            'max_age_days': pw_policy.get('MaxPasswordAge', 0),
            'password_reuse_prevention': pw_policy.get('PasswordReusePrevention', 0),
        }
    elif isinstance(pw_policy, dict) and '_error' in pw_policy:
        result['password_policy'] = pw_policy
    else:
        result['password_policy'] = {'_note': 'No custom password policy set (using AWS defaults)'}

    cred_report = safe_call(lambda: _get_credential_report(iam))
    if isinstance(cred_report, dict) and '_error' in cred_report:
        result['credential_report'] = cred_report
    elif isinstance(cred_report, list):
        mfa_enabled = sum(1 for u in cred_report if u.get('mfa_active') == 'true')
        mfa_disabled = sum(1 for u in cred_report if u.get('mfa_active') == 'false')
        root_mfa = 'unknown'
        for u in cred_report:
            if u.get('user') == '<root_account>':
                root_mfa = u.get('mfa_active', 'unknown')
                break
        result['credential_report'] = {
            'total_users': len(cred_report),
            'mfa_enabled': mfa_enabled,
            'mfa_disabled': mfa_disabled,
            'root_mfa_enabled': root_mfa,
        }
    else:
        result['credential_report'] = {'_error': 'Unexpected format'}

    return result


def _get_credential_report(iam):
    gen = safe_call(lambda: iam.generate_credential_report())
    if isinstance(gen, dict) and '_error' in gen:
        return gen
    import time
    for _ in range(10):
        report = safe_call(lambda: iam.get_credential_report())
        if isinstance(report, dict) and '_error' in report:
            return report
        if isinstance(report, dict) and 'Content' in report:
            content = report['Content']
            if isinstance(content, bytes):
                decoded = content.decode('utf-8')
            else:
                decoded = base64.b64decode(content).decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return list(reader)
        state = report.get('State', '') if isinstance(report, dict) else ''
        if state == 'COMPLETE':
            break
        time.sleep(2)
    return {'_error': 'Credential report generation timed out'}


def scan_s3_public_access(session):
    s3control = session.client('s3control', region_name=REGION)
    sts = session.client('sts')
    acct_id = safe_call(lambda: sts.get_caller_identity()['Account'], 'unknown')
    if isinstance(acct_id, dict) and '_error' in acct_id:
        return acct_id

    block = safe_call(lambda: s3control.get_public_access_block(
        AccountId=acct_id
    )['PublicAccessBlockConfiguration'])
    if isinstance(block, dict) and '_error' not in block:
        return {
            'account_id': acct_id,
            'block_public_acls': block.get('BlockPublicAcls', False),
            'ignore_public_acls': block.get('IgnorePublicAcls', False),
            'block_public_policy': block.get('BlockPublicPolicy', False),
            'restrict_public_buckets': block.get('RestrictPublicBuckets', False),
            'all_blocked': all([
                block.get('BlockPublicAcls', False),
                block.get('IgnorePublicAcls', False),
                block.get('BlockPublicPolicy', False),
                block.get('RestrictPublicBuckets', False),
            ]),
        }
    elif isinstance(block, dict) and '_error' in block:
        return block
    return {'_note': 'No account-level public access block configured', 'account_id': acct_id}


def scan_config_compliance(session):
    config = session.client('config', region_name=REGION)
    rules = safe_call(lambda: config.describe_compliance_by_config_rule().get(
        'ComplianceByConfigRules', []), [])
    if isinstance(rules, dict) and '_error' in rules:
        return rules
    if not rules:
        return {'_note': 'AWS Config not enabled or no rules configured'}

    summary = {'compliant': 0, 'non_compliant': 0, 'not_applicable': 0, 'insufficient_data': 0}
    non_compliant_rules = []
    for rule in rules:
        ct = rule.get('Compliance', {}).get('ComplianceType', 'INSUFFICIENT_DATA')
        if ct == 'COMPLIANT':
            summary['compliant'] += 1
        elif ct == 'NON_COMPLIANT':
            summary['non_compliant'] += 1
            non_compliant_rules.append(rule.get('ConfigRuleName', ''))
        elif ct == 'NOT_APPLICABLE':
            summary['not_applicable'] += 1
        else:
            summary['insufficient_data'] += 1

    return {
        'total_rules': len(rules),
        'summary': summary,
        'non_compliant_rules': non_compliant_rules[:50],
    }


def scan_secrets_manager(session):
    sm = session.client('secretsmanager', region_name=REGION)
    secrets = []
    paginator = sm.get_paginator('list_secrets')

    raw = safe_call(lambda: list(paginator.paginate(MaxResults=100)))
    if isinstance(raw, dict) and '_error' in raw:
        return raw

    for page in (raw or []):
        for s in page.get('SecretList', []):
            secrets.append({
                'name': s.get('Name', ''),
                'rotation_enabled': s.get('RotationEnabled', False),
                'rotation_lambda': s.get('RotationLambdaARN', ''),
                'last_rotated': s.get('LastRotatedDate', ''),
                'last_accessed': s.get('LastAccessedDate', ''),
            })

    rotation_on = sum(1 for s in secrets if s.get('rotation_enabled'))
    rotation_off = len(secrets) - rotation_on
    return {
        'total_secrets': len(secrets),
        'rotation_enabled': rotation_on,
        'rotation_disabled': rotation_off,
        'secrets': secrets,
    }


def scan_account(profile):
    print(f"\n  [{profile}]", flush=True)
    session = boto3.Session(profile_name=profile)
    blocked_apis = []
    data = {'profile': profile}

    print(f"    GuardDuty ...", end='', flush=True)
    gd = scan_guardduty(session)
    data['guardduty'] = gd
    if isinstance(gd, dict) and '_error' in gd:
        blocked_apis.append(f"GuardDuty: {gd['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        det_count = len(gd.get('detectors', []))
        print(f" {det_count} detectors, findings: {gd.get('finding_stats', {})}", flush=True)

    print(f"    ACM ...", end='', flush=True)
    acm = scan_acm(session)
    data['acm'] = acm
    if isinstance(acm, dict) and '_error' in acm:
        blocked_apis.append(f"ACM: {acm['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {acm.get('total', 0)} certificates", flush=True)

    print(f"    IAM ...", end='', flush=True)
    iam = scan_iam(session)
    data['iam'] = iam
    cred = iam.get('credential_report', {})
    if isinstance(cred, dict) and '_error' in cred:
        blocked_apis.append(f"IAM credential report: {cred['_error']}")
    print(f" users_mfa={cred.get('mfa_enabled','?')}/{cred.get('total_users','?')}", flush=True)

    print(f"    S3 Public Access Block ...", end='', flush=True)
    s3 = scan_s3_public_access(session)
    data['s3_public_access_block'] = s3
    if isinstance(s3, dict) and '_error' in s3:
        blocked_apis.append(f"S3 control: {s3['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" all_blocked={s3.get('all_blocked', 'N/A')}", flush=True)

    print(f"    Config Compliance ...", end='', flush=True)
    cfg = scan_config_compliance(session)
    data['config_compliance'] = cfg
    if isinstance(cfg, dict) and '_error' in cfg:
        blocked_apis.append(f"Config: {cfg['_error']}")
        print(f" BLOCKED", flush=True)
    elif '_note' in cfg:
        print(f" {cfg['_note']}", flush=True)
    else:
        s = cfg.get('summary', {})
        print(f" {cfg.get('total_rules',0)} rules, {s.get('non_compliant',0)} non-compliant", flush=True)

    print(f"    Secrets Manager ...", end='', flush=True)
    sm = scan_secrets_manager(session)
    data['secrets_manager'] = sm
    if isinstance(sm, dict) and '_error' in sm:
        blocked_apis.append(f"Secrets Manager: {sm['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {sm.get('total_secrets',0)} secrets, {sm.get('rotation_disabled',0)} without rotation", flush=True)

    data['blocked_apis'] = blocked_apis
    return data


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    print("=== AWS Security Posture Scan ===", flush=True)
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

    # Date serialization for secrets timestamps
    outpath = 'inventory/aws/security_posture.json'
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Wrote {outpath}", flush=True)

    print("\n=== Summary ===", flush=True)
    for profile, data in results.items():
        blocked = data.get('blocked_apis', [])
        print(f"\n  {profile}:", flush=True)
        if blocked:
            print(f"    Blocked APIs ({len(blocked)}): {', '.join(blocked)}", flush=True)
        gd = data.get('guardduty', {})
        if not isinstance(gd, dict) or '_error' not in gd:
            print(f"    GuardDuty: {len(gd.get('detectors',[]))} detectors, severity counts={gd.get('finding_stats',{})}", flush=True)
        acm = data.get('acm', {})
        if not isinstance(acm, dict) or '_error' not in acm:
            print(f"    ACM: {acm.get('total',0)} certs", flush=True)
        iam = data.get('iam', {})
        cr = iam.get('credential_report', {})
        if isinstance(cr, dict) and '_error' not in cr:
            print(f"    IAM: {cr.get('total_users',0)} users, {cr.get('mfa_enabled',0)} MFA on, root_mfa={cr.get('root_mfa_enabled','?')}", flush=True)
        s3 = data.get('s3_public_access_block', {})
        if isinstance(s3, dict) and '_error' not in s3:
            print(f"    S3: public_access_all_blocked={s3.get('all_blocked','N/A')}", flush=True)
        sm = data.get('secrets_manager', {})
        if isinstance(sm, dict) and '_error' not in sm:
            print(f"    Secrets: {sm.get('total_secrets',0)} total, {sm.get('rotation_disabled',0)} without rotation", flush=True)

    print("\nDone.", flush=True)
