#!/usr/bin/env python3
"""AWS cost optimization analysis — RI/SP utilization, cost trending, forecasting."""

import boto3
import json
import os
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from botocore.exceptions import ClientError

MGMT_PROFILE = 'mm-madmobile-mgmt'

ACCOUNTS = [
    'mm-retail-prod-us',
    'mm-payments-prod-us',
    'mm-cake-development',
    'mm-shared-services',
    'mm-retail-prod-eu',
    'mm-retail-prod-apac',
    'mm-retail-prod-us-dr',
    'mm-customer-analytics',
    'mm-shared-artifact-registry',
    'mm-security',
    'mm-monvia',
    'mm-menupad-prod-metro',
    'mm-marketplace-seller',
    'mm-cake-r-and-d',
    'mm-forensics',
    'mm-dns-management',
    'mm-mm-archive',
]


def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess',
                     'AuthorizationError', 'OptInRequired', 'SubscriptionRequiredException',
                     'BillingAccessDeniedException'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}


def month_start(dt):
    return dt.replace(day=1).strftime('%Y-%m-%d')


def get_savings_plans_utilization(ce, start, end):
    return safe_call(lambda: ce.get_savings_plans_utilization(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
    ))


def get_reservation_utilization(ce, start, end):
    return safe_call(lambda: ce.get_reservation_utilization(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
    ))


def get_cost_and_usage(ce, start, end):
    results = []
    next_token = None
    while True:
        kwargs = {
            'TimePeriod': {'Start': start, 'End': end},
            'Granularity': 'MONTHLY',
            'Metrics': ['UnblendedCost', 'UsageQuantity'],
            'GroupBy': [
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
            ],
        }
        if next_token:
            kwargs['NextPageToken'] = next_token

        resp = safe_call(lambda: ce.get_cost_and_usage(**kwargs))
        if isinstance(resp, dict) and '_error' in resp:
            return resp

        results.extend(resp.get('ResultsByTime', []))
        next_token = resp.get('NextPageToken')
        if not next_token:
            break
    return results


def get_cost_and_usage_single(ce, start, end):
    """Simpler query for individual accounts (no LINKED_ACCOUNT grouping)."""
    results = []
    next_token = None
    while True:
        kwargs = {
            'TimePeriod': {'Start': start, 'End': end},
            'Granularity': 'MONTHLY',
            'Metrics': ['UnblendedCost'],
            'GroupBy': [{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
        }
        if next_token:
            kwargs['NextPageToken'] = next_token

        resp = safe_call(lambda: ce.get_cost_and_usage(**kwargs))
        if isinstance(resp, dict) and '_error' in resp:
            return resp

        results.extend(resp.get('ResultsByTime', []))
        next_token = resp.get('NextPageToken')
        if not next_token:
            break
    return results


def get_cost_forecast(ce, start, end):
    return safe_call(lambda: ce.get_cost_forecast(
        TimePeriod={'Start': start, 'End': end},
        Metric='UNBLENDED_COST',
        Granularity='MONTHLY',
    ))


def analyze_cost_trends(cost_data):
    """Build monthly totals and top-services from cost_and_usage results."""
    monthly_totals = defaultdict(float)
    service_totals = defaultdict(float)
    account_totals = defaultdict(float)
    monthly_by_account = defaultdict(lambda: defaultdict(float))

    for period in cost_data:
        month = period.get('TimePeriod', {}).get('Start', '')
        for group in period.get('Groups', []):
            keys = group.get('Keys', [])
            amount = float(group.get('Metrics', {}).get('UnblendedCost', {}).get('Amount', 0))
            if amount < 0.01:
                continue

            service = keys[0] if keys else 'Unknown'
            account = keys[1] if len(keys) > 1 else 'single'

            monthly_totals[month] += amount
            service_totals[service] += amount
            account_totals[account] += amount
            monthly_by_account[month][account] += amount

    sorted_months = sorted(monthly_totals.keys())
    trend = "stable"
    if len(sorted_months) >= 3:
        first_half = sum(monthly_totals[m] for m in sorted_months[:len(sorted_months)//2])
        second_half = sum(monthly_totals[m] for m in sorted_months[len(sorted_months)//2:])
        months_first = len(sorted_months) // 2
        months_second = len(sorted_months) - months_first
        if months_first > 0 and months_second > 0:
            avg_first = first_half / months_first
            avg_second = second_half / months_second
            if avg_second > avg_first * 1.1:
                trend = "increasing"
            elif avg_second < avg_first * 0.9:
                trend = "decreasing"

    return {
        'monthly_totals': {m: round(monthly_totals[m], 2) for m in sorted_months},
        'top_services': dict(sorted(
            ((k, round(v, 2)) for k, v in service_totals.items()),
            key=lambda x: -x[1]
        )[:25]),
        'account_totals': dict(sorted(
            ((k, round(v, 2)) for k, v in account_totals.items()),
            key=lambda x: -x[1]
        )),
        'trend': trend,
        'total_spend': round(sum(monthly_totals.values()), 2),
    }


def analyze_sp_utilization(sp_data):
    if isinstance(sp_data, dict) and '_error' in sp_data:
        return sp_data

    periods = []
    for period in sp_data.get('SavingsPlansUtilizationsByTime', []):
        util = period.get('Utilization', {})
        periods.append({
            'month': period.get('TimePeriod', {}).get('Start', ''),
            'utilization_pct': util.get('UtilizationPercentage', '0'),
            'total_commitment': util.get('TotalCommitment', '0'),
            'used_commitment': util.get('UsedCommitment', '0'),
            'unused_commitment': util.get('UnusedCommitment', '0'),
            'savings_vs_on_demand_pct': util.get('NetSavings', '0'),
        })

    total = sp_data.get('Total', {}).get('Utilization', {})
    return {
        'periods': periods,
        'overall_utilization_pct': total.get('UtilizationPercentage', 'N/A'),
        'total_commitment': total.get('TotalCommitment', 'N/A'),
        'net_savings': total.get('NetSavings', 'N/A'),
    }


def analyze_ri_utilization(ri_data):
    if isinstance(ri_data, dict) and '_error' in ri_data:
        return ri_data

    periods = []
    for period in ri_data.get('UtilizationsByTime', []):
        total = period.get('Total', {})
        periods.append({
            'month': period.get('TimePeriod', {}).get('Start', ''),
            'utilization_pct': total.get('UtilizationPercentage', '0'),
            'purchased_hours': total.get('PurchasedHours', '0'),
            'total_actual_hours': total.get('TotalActualHours', '0'),
            'unused_hours': total.get('UnusedHours', '0'),
            'net_savings': total.get('NetRISavings', '0'),
        })

    total = ri_data.get('Total', {})
    return {
        'periods': periods,
        'overall_utilization_pct': total.get('UtilizationPercentage', 'N/A'),
        'net_savings': total.get('NetRISavings', 'N/A'),
    }


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)
    now = datetime.now(timezone.utc)

    six_months_ago = month_start(now - timedelta(days=180))
    three_months_ago = month_start(now - timedelta(days=90))
    current_month_start = month_start(now)
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    thirty_days_out = (now + timedelta(days=30)).strftime('%Y-%m-%d')

    output = {
        'generated_at': now.isoformat(),
        'management_profile': MGMT_PROFILE,
        'errors': {},
    }

    print("=== AWS Cost Optimization Analysis ===", flush=True)
    print(f"  Management account: {MGMT_PROFILE}", flush=True)
    print(f"  Cost window: {six_months_ago} to {current_month_start}", flush=True)
    print(f"  RI/SP window: {three_months_ago} to {current_month_start}", flush=True)

    session = boto3.Session(profile_name=MGMT_PROFILE)
    ce = session.client('ce', region_name='us-east-1')

    # --- Savings Plans Utilization ---
    print("\n--- Savings Plans Utilization (last 3 months) ---", flush=True)
    sp_raw = get_savings_plans_utilization(ce, three_months_ago, current_month_start)
    sp_result = analyze_sp_utilization(sp_raw)
    if isinstance(sp_result, dict) and '_error' in sp_result:
        print(f"  {sp_result['_error']}", flush=True)
        output['errors']['savings_plans'] = sp_result['_error']
    else:
        print(f"  Overall utilization: {sp_result.get('overall_utilization_pct', 'N/A')}%", flush=True)
        print(f"  Total commitment: ${sp_result.get('total_commitment', 'N/A')}", flush=True)
        print(f"  Net savings: ${sp_result.get('net_savings', 'N/A')}", flush=True)
    output['savings_plans'] = sp_result

    # --- Reserved Instance Utilization ---
    print("\n--- Reserved Instance Utilization (last 3 months) ---", flush=True)
    ri_raw = get_reservation_utilization(ce, three_months_ago, current_month_start)
    ri_result = analyze_ri_utilization(ri_raw)
    if isinstance(ri_result, dict) and '_error' in ri_result:
        print(f"  {ri_result['_error']}", flush=True)
        output['errors']['reserved_instances'] = ri_result['_error']
    else:
        print(f"  Overall utilization: {ri_result.get('overall_utilization_pct', 'N/A')}%", flush=True)
        print(f"  Net savings: ${ri_result.get('net_savings', 'N/A')}", flush=True)
    output['reserved_instances'] = ri_result

    # --- Cost and Usage (management account, org-wide) ---
    print("\n--- Cost & Usage by Service+Account (last 6 months) ---", flush=True)
    cost_data = get_cost_and_usage(ce, six_months_ago, current_month_start)

    mgmt_access_denied = isinstance(cost_data, dict) and '_error' in cost_data

    if mgmt_access_denied:
        print(f"  Management account denied: {cost_data['_error']}", flush=True)
        output['errors']['cost_usage_mgmt'] = cost_data['_error']

        print("  Falling back to individual account queries ...", flush=True)
        all_cost_data = []
        for profile in ACCOUNTS:
            print(f"    {profile} ... ", end='', flush=True)
            try:
                acct_session = boto3.Session(profile_name=profile)
                acct_ce = acct_session.client('ce', region_name='us-east-1')
                acct_costs = get_cost_and_usage_single(acct_ce, six_months_ago, current_month_start)
                if isinstance(acct_costs, dict) and '_error' in acct_costs:
                    print(f"ERROR: {acct_costs['_error']}", flush=True)
                    output['errors'][f'cost_{profile}'] = acct_costs['_error']
                else:
                    for period in acct_costs:
                        for group in period.get('Groups', []):
                            group['Keys'].append(profile)
                    all_cost_data.extend(acct_costs)
                    months = len(acct_costs)
                    print(f"{months} months", flush=True)
            except Exception as e:
                print(f"ERROR: {e}", flush=True)
                output['errors'][f'cost_{profile}'] = str(e)
        cost_data = all_cost_data

    if not (isinstance(cost_data, dict) and '_error' in cost_data):
        trends = analyze_cost_trends(cost_data)
        print(f"\n  Total spend (period): ${trends['total_spend']:,.2f}", flush=True)
        print(f"  Trend: {trends['trend']}", flush=True)
        print(f"  Monthly totals:", flush=True)
        for m, v in trends['monthly_totals'].items():
            print(f"    {m}: ${v:,.2f}", flush=True)
        print(f"  Top 10 services:", flush=True)
        for svc, cost in list(trends['top_services'].items())[:10]:
            print(f"    {svc}: ${cost:,.2f}", flush=True)
        output['cost_trends'] = trends
    else:
        output['cost_trends'] = cost_data

    # --- Cost Forecast ---
    print("\n--- Cost Forecast (next 30 days) ---", flush=True)
    forecast = get_cost_forecast(ce, tomorrow, thirty_days_out)
    if isinstance(forecast, dict) and '_error' in forecast:
        print(f"  {forecast['_error']}", flush=True)
        output['errors']['forecast'] = forecast['_error']
        output['forecast'] = forecast
    else:
        total_forecast = forecast.get('Total', {})
        output['forecast'] = {
            'period': f"{tomorrow} to {thirty_days_out}",
            'total_amount': total_forecast.get('Amount', 'N/A'),
            'unit': total_forecast.get('Unit', 'USD'),
            'by_period': [{
                'start': fp.get('TimePeriod', {}).get('Start', ''),
                'end': fp.get('TimePeriod', {}).get('End', ''),
                'mean': fp.get('MeanValue', ''),
                'min': fp.get('PredictionIntervalLowerBound', ''),
                'max': fp.get('PredictionIntervalUpperBound', ''),
            } for fp in forecast.get('ForecastResultsByTime', [])],
        }
        print(f"  Forecasted total: ${total_forecast.get('Amount', 'N/A')} {total_forecast.get('Unit', '')}", flush=True)

    # --- Write output ---
    outpath = 'inventory/aws/cost_optimization.json'
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Wrote {outpath}", flush=True)

    # --- Summary ---
    print("\n=== Summary ===", flush=True)
    if output['errors']:
        print(f"  {len(output['errors'])} access errors encountered", flush=True)
        for k, v in output['errors'].items():
            print(f"    {k}: {v}", flush=True)
    else:
        print("  No access errors", flush=True)

    print("\nDone.", flush=True)
