#!/usr/bin/env python3
"""AWS CloudTrail deployment activity analysis across production accounts."""

import boto3
import json
import os
from datetime import datetime, timezone, timedelta
from collections import defaultdict
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

ACCOUNTS = [
    'mm-retail-prod-us',
    'mm-payments-prod-us',
    'mm-cake-development',
    'mm-shared-services',
    'mm-retail-prod-eu',
    'mm-retail-prod-apac',
]

REGIONS = ['us-east-1', 'us-west-2']

DEPLOY_EVENTS = {
    'UpdateService',
    'CreateDeployment',
    'StartPipelineExecution',
    'StartBuild',
    'UpdateFunctionCode',
    'UpdateStack',
    'RunTask',
    'RegisterTaskDefinition',
}

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def lookup_events(profile, region, start_time, end_time):
    """Page through CloudTrail LookupEvents for deployment-signal event names."""
    session = boto3.Session(profile_name=profile)
    ct = session.client('cloudtrail', region_name=region)
    events = []

    for event_name in DEPLOY_EVENTS:
        next_token = None
        while True:
            kwargs = {
                'LookupAttributes': [
                    {'AttributeKey': 'EventName', 'AttributeValue': event_name}
                ],
                'StartTime': start_time,
                'EndTime': end_time,
                'MaxResults': 50,
            }
            if next_token:
                kwargs['NextToken'] = next_token

            result = safe_call(lambda: ct.lookup_events(**kwargs))
            if isinstance(result, dict) and '_error' in result:
                return result

            for ev in result.get('Events', []):
                ts = ev.get('EventTime')
                if ts and hasattr(ts, 'isoformat'):
                    ts = ts.isoformat()
                events.append({
                    'timestamp': ts,
                    'event_name': ev.get('EventName', ''),
                    'username': ev.get('Username', ''),
                    'source_ip': ev.get('CloudTrailEvent', ''),
                    'account': profile,
                    'region': region,
                })

            next_token = result.get('NextToken')
            if not next_token:
                break

    # Extract source_ip from the raw CloudTrailEvent JSON blob
    for ev in events:
        raw = ev.pop('source_ip', '')
        if raw:
            try:
                detail = json.loads(raw)
                ev['source_ip'] = detail.get('sourceIPAddress', '')
                if not ev['username']:
                    ident = detail.get('userIdentity', {})
                    ev['username'] = ident.get('arn', ident.get('principalId', ''))
            except (json.JSONDecodeError, TypeError):
                ev['source_ip'] = ''

    return events


def aggregate(all_events):
    by_account = defaultdict(int)
    by_day_of_week = defaultdict(int)
    by_hour = defaultdict(int)
    by_principal = defaultdict(int)
    by_event_type = defaultdict(int)
    by_account_event = defaultdict(lambda: defaultdict(int))

    for ev in all_events:
        acct = ev['account']
        by_account[acct] += 1
        by_event_type[ev['event_name']] += 1
        by_principal[ev['username']] += 1
        by_account_event[acct][ev['event_name']] += 1

        ts_str = ev.get('timestamp', '')
        if ts_str:
            try:
                dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                by_day_of_week[DAY_NAMES[dt.weekday()]] += 1
                by_hour[dt.hour] += 1
            except (ValueError, TypeError):
                pass

    return {
        'by_account': dict(sorted(by_account.items(), key=lambda x: -x[1])),
        'by_day_of_week': {d: by_day_of_week.get(d, 0) for d in DAY_NAMES},
        'by_hour_of_day': {str(h): by_hour.get(h, 0) for h in range(24)},
        'by_principal': dict(sorted(by_principal.items(), key=lambda x: -x[1])[:30]),
        'by_event_type': dict(sorted(by_event_type.items(), key=lambda x: -x[1])),
        'by_account_event': {k: dict(v) for k, v in by_account_event.items()},
    }


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=90)

    print(f"=== CloudTrail Deployment Activity ===", flush=True)
    print(f"  Window: {start_time.date()} to {end_time.date()}", flush=True)
    print(f"  Accounts: {len(ACCOUNTS)}, Regions: {len(REGIONS)}", flush=True)

    all_events = []
    errors = {}

    for profile in ACCOUNTS:
        for region in REGIONS:
            label = f"{profile}/{region}"
            print(f"\n  Querying {label} ...", end='', flush=True)
            result = lookup_events(profile, region, start_time, end_time)
            if isinstance(result, dict) and '_error' in result:
                errors[label] = result['_error']
                print(f" ERROR: {result['_error']}", flush=True)
            else:
                all_events.extend(result)
                print(f" {len(result)} events", flush=True)

    print(f"\n=== Totals ===", flush=True)
    print(f"  {len(all_events)} deployment events across {len(ACCOUNTS)} accounts", flush=True)
    print(f"  {len(errors)} account/region combos had errors", flush=True)

    agg = aggregate(all_events)

    output = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'window_start': start_time.isoformat(),
        'window_end': end_time.isoformat(),
        'total_events': len(all_events),
        'errors': errors,
        'aggregations': agg,
        'events': all_events,
    }

    outpath = 'inventory/aws/cloudtrail_deployments.json'
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Wrote {outpath}", flush=True)

    print("\n=== Summary by Account ===", flush=True)
    for acct, count in agg['by_account'].items():
        print(f"    {acct}: {count}", flush=True)

    print("\n=== Summary by Event Type ===", flush=True)
    for etype, count in agg['by_event_type'].items():
        print(f"    {etype}: {count}", flush=True)

    if errors:
        print("\n=== Errors ===", flush=True)
        for label, err in errors.items():
            print(f"    {label}: {err}", flush=True)

    print("\nDone.", flush=True)
