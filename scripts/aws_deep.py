#!/usr/bin/env python3
"""AWS deep analysis — Route53 zones, ECS services, Security Hub findings."""

import boto3
import json
import os
import glob
from botocore.exceptions import ClientError

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


def get_route53_zones():
    session = boto3.Session(profile_name='mm-dns-management')
    r53 = session.client('route53')
    zones = safe_call(lambda: r53.list_hosted_zones()['HostedZones'], [])
    if isinstance(zones, dict) and '_error' in zones:
        return zones
    results = []
    for z in zones:
        zone_id = z['Id'].split('/')[-1]
        record_count = z.get('ResourceRecordSetCount', 0)
        results.append({
            'id': zone_id,
            'name': z['Name'],
            'private': z['Config'].get('PrivateZone', False),
            'record_count': record_count,
        })
    return results


def get_ecs_services():
    results = {}
    inventory_files = glob.glob('inventory/aws/mm-*.json')
    for f in inventory_files:
        with open(f) as fh:
            data = json.load(fh)
        profile = data.get('profile', '')
        for region, rdata in data.get('regions', {}).items():
            if not isinstance(rdata, dict):
                continue
            clusters = rdata.get('ecs_clusters', [])
            if isinstance(clusters, dict) or not clusters:
                continue
            for cluster_arn in clusters:
                if not isinstance(cluster_arn, str):
                    continue
                cluster_name = cluster_arn.split('/')[-1]
                try:
                    session = boto3.Session(profile_name=profile)
                    ecs = session.client('ecs', region_name=region)
                    svc_arns = ecs.list_services(cluster=cluster_arn, maxResults=100).get('serviceArns', [])
                    if svc_arns:
                        svcs = ecs.describe_services(cluster=cluster_arn, services=svc_arns[:10])
                        svc_details = [{
                            'name': s['serviceName'],
                            'status': s['status'],
                            'desired': s.get('desiredCount', 0),
                            'running': s.get('runningCount', 0),
                            'launch_type': s.get('launchType', 'unknown'),
                        } for s in svcs.get('services', [])]
                    else:
                        svc_details = []
                    key = f"{profile}/{region}/{cluster_name}"
                    results[key] = {
                        'profile': profile, 'region': region,
                        'cluster': cluster_name,
                        'service_count': len(svc_arns),
                        'services': svc_details,
                    }
                except Exception as e:
                    results[f"{profile}/{region}/{cluster_name}"] = {'error': str(e)}
    return results


def get_security_findings():
    session = boto3.Session(profile_name='mm-security')
    sh = session.client('securityhub', region_name='us-east-1')
    return safe_call(lambda: {
        'critical': sh.get_findings(
            Filters={'SeverityLabel': [{'Value': 'CRITICAL', 'Comparison': 'EQUALS'}],
                     'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}]},
            MaxResults=1
        ).get('Findings', [{'_count_unavailable': True}]),
        'high': sh.get_findings(
            Filters={'SeverityLabel': [{'Value': 'HIGH', 'Comparison': 'EQUALS'}],
                     'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}]},
            MaxResults=1
        ).get('Findings', [{'_count_unavailable': True}]),
    }, {'_error': 'Security Hub access denied'})


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    print("=== Route53 Zones ===", flush=True)
    zones = get_route53_zones()
    if isinstance(zones, list):
        print(f"  {len(zones)} hosted zones", flush=True)
        for z in zones:
            print(f"    {z['name']} ({z['record_count']} records, {'private' if z['private'] else 'public'})")
    else:
        print(f"  Error: {zones}", flush=True)
    with open('inventory/aws/route53_zones.json', 'w') as f:
        json.dump(zones, f, indent=2)

    print("\n=== ECS Services ===", flush=True)
    ecs = get_ecs_services()
    total_services = sum(v.get('service_count', 0) for v in ecs.values() if isinstance(v, dict) and 'service_count' in v)
    print(f"  {len(ecs)} clusters, {total_services} services total", flush=True)
    with open('inventory/aws/ecs_services.json', 'w') as f:
        json.dump(ecs, f, indent=2)

    print("\n=== Security Hub Findings ===", flush=True)
    findings = get_security_findings()
    print(f"  {findings}", flush=True)
    with open('inventory/aws/security_findings.json', 'w') as f:
        json.dump(findings, f, indent=2, default=str)

    print("\nDone.", flush=True)
