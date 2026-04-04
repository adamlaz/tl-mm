#!/usr/bin/env python3
"""Fetch CloudWatch dashboard definitions and parse widget/metric/alarm details."""

import boto3
import json
import os
from collections import defaultdict
from datetime import datetime
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


PROFILES_REGIONS = {
    'mm-retail-prod-us': ['us-east-1', 'us-west-2'],
    'mm-cake-r-and-d': ['us-east-1'],
}

os.makedirs('inventory/aws', exist_ok=True)


def extract_metrics_from_widget(widget):
    """Extract metric namespaces and alarm ARNs from a dashboard widget."""
    namespaces = set()
    alarm_arns = set()
    metric_names = set()

    props = widget.get("properties", {})

    for metric_entry in props.get("metrics", []):
        if isinstance(metric_entry, list) and len(metric_entry) >= 2:
            namespaces.add(metric_entry[0])
            if len(metric_entry) >= 2:
                metric_names.add(metric_entry[1])

    for annotation_axis in props.get("annotations", {}).get("alarms", []):
        if isinstance(annotation_axis, str) and "arn:aws:cloudwatch" in annotation_axis:
            alarm_arns.add(annotation_axis)

    for ann_list_key in ["horizontal", "vertical"]:
        for ann in props.get("annotations", {}).get(ann_list_key, []):
            if isinstance(ann, dict) and "value" in ann:
                pass

    if props.get("alarms"):
        for a in props["alarms"]:
            if isinstance(a, str):
                alarm_arns.add(a)

    return namespaces, alarm_arns, metric_names


def parse_dashboard_body(body_json):
    """Parse a dashboard JSON body string into widget/metric/alarm summary."""
    try:
        body = json.loads(body_json)
    except (json.JSONDecodeError, TypeError):
        return {"parse_error": "Invalid JSON body"}

    widgets = body.get("widgets", [])
    all_namespaces = set()
    all_alarms = set()
    all_metrics = set()
    widget_types = defaultdict(int)

    for w in widgets:
        wtype = w.get("type", "unknown")
        widget_types[wtype] += 1

        ns, alarms, metrics = extract_metrics_from_widget(w)
        all_namespaces.update(ns)
        all_alarms.update(alarms)
        all_metrics.update(metrics)

    return {
        "widget_count": len(widgets),
        "widget_types": dict(widget_types),
        "metric_namespaces": sorted(all_namespaces),
        "metric_names": sorted(all_metrics),
        "alarm_arns": sorted(all_alarms),
        "alarm_count": len(all_alarms),
    }


def collect_dashboards(profile, region):
    """List and describe all CloudWatch dashboards for a profile/region."""
    session = boto3.Session(profile_name=profile)
    cw = session.client('cloudwatch', region_name=region)

    names_result = safe_call(lambda: cw.list_dashboards())
    if isinstance(names_result, dict) and '_error' in names_result:
        return [], [f"{profile}/{region}: {names_result['_error']}"]

    dashboard_entries = names_result.get('DashboardEntries', [])
    if not dashboard_entries:
        return [], []

    results = []
    errors = []

    for entry in dashboard_entries:
        dash_name = entry.get('DashboardName', '')
        print(f"    Fetching dashboard: {dash_name}...", flush=True)

        detail = safe_call(lambda n=dash_name: cw.get_dashboard(DashboardName=n))
        if isinstance(detail, dict) and '_error' in detail:
            errors.append(f"{profile}/{region}/{dash_name}: {detail['_error']}")
            results.append({
                "name": dash_name,
                "profile": profile,
                "region": region,
                "size": entry.get('Size', 0),
                "last_modified": entry.get('LastModified', ''),
                "_error": detail['_error'],
            })
            continue

        body_json = detail.get('DashboardBody', '{}')
        parsed = parse_dashboard_body(body_json)

        results.append({
            "name": dash_name,
            "profile": profile,
            "region": region,
            "arn": detail.get('DashboardArn', ''),
            "size": entry.get('Size', 0),
            "last_modified": entry.get('LastModified', ''),
            **parsed,
        })

    return results, errors


def main():
    all_dashboards = []
    all_errors = []

    print("=" * 60)
    print("CloudWatch Dashboard Analysis")
    print("=" * 60)

    for profile, regions in PROFILES_REGIONS.items():
        for region in regions:
            tag = f"{profile}/{region}"
            print(f"\n[CloudWatch] {tag} ...", flush=True)

            dashboards, errors = collect_dashboards(profile, region)
            if dashboards:
                print(f"  -> {len(dashboards)} dashboard(s)", flush=True)
            else:
                print(f"  -> No dashboards found", flush=True)

            all_dashboards.extend(dashboards)
            all_errors.extend(errors)

    all_namespaces = set()
    all_alarms = set()
    total_widgets = 0
    for d in all_dashboards:
        total_widgets += d.get("widget_count", 0)
        all_namespaces.update(d.get("metric_namespaces", []))
        all_alarms.update(d.get("alarm_arns", []))

    by_profile = defaultdict(list)
    for d in all_dashboards:
        by_profile[d["profile"]].append(d["name"])

    output = {
        "extracted_at": datetime.now().isoformat(),
        "summary": {
            "total_dashboards": len(all_dashboards),
            "total_widgets": total_widgets,
            "total_alarm_references": len(all_alarms),
            "all_metric_namespaces": sorted(all_namespaces),
            "dashboards_by_profile": dict(by_profile),
        },
        "dashboards": all_dashboards,
        "errors": all_errors,
    }

    out_path = 'inventory/aws/cloudwatch_dashboards.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total dashboards:       {len(all_dashboards)}")
    print(f"Total widgets:          {total_widgets}")
    print(f"Alarm references:       {len(all_alarms)}")
    print(f"Metric namespaces:      {', '.join(sorted(all_namespaces)) or 'none'}")

    print(f"\nDashboards per profile:")
    for profile, names in sorted(by_profile.items()):
        print(f"  {profile}: {', '.join(names)}")

    print(f"\nDashboard details:")
    for d in all_dashboards:
        error_note = f" [ERROR: {d.get('_error', '')}]" if '_error' in d else ""
        print(f"  {d['profile']}/{d['name']}: "
              f"{d.get('widget_count', '?')} widgets, "
              f"{len(d.get('metric_namespaces', []))} namespaces, "
              f"{d.get('alarm_count', 0)} alarms"
              f"{error_note}")

    if all_errors:
        print(f"\nErrors ({len(all_errors)}):")
        for e in all_errors:
            print(f"  - {e}")
    print()


if __name__ == '__main__':
    main()
