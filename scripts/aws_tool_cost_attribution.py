#!/usr/bin/env python3
"""Attribute AWS costs to identified tools by service and EC2 tag analysis."""

import boto3
import json
import os
import re
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, NoCredentialsError

TOOL_PATTERNS = {
    "Jenkins": ["jenkins", "ci-server", "build-server"],
    "Grafana": ["grafana", "mimir", "loki", "tempo"],
    "Kafka": ["kafka", "zookeeper"],
    "Elasticsearch": ["elasticsearch", "elastic", "es-data", "es-master"],
    "Keycloak": ["keycloak", "identity"],
    "Neo4j": ["neo4j", "graph-db"],
    "RabbitMQ": ["rabbitmq", "mq-broker"],
    "Docker Build": ["dockerpos", "docker-build"],
}


def get_profiles():
    config_path = os.path.expanduser("~/.aws/config")
    profiles = []
    with open(config_path) as f:
        for line in f:
            m = re.match(r"\[profile (mm-[^\]]+)\]", line)
            if m:
                profiles.append(m.group(1))
    return profiles


def get_cost_by_service(session):
    try:
        ce = session.client("ce", region_name="us-east-1")
        end = datetime.now().replace(day=1)
        start = (end - timedelta(days=32)).replace(day=1)
        resp = ce.get_cost_and_usage(
            TimePeriod={"Start": start.strftime("%Y-%m-%d"), "End": end.strftime("%Y-%m-%d")},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        services = []
        for g in resp.get("ResultsByTime", [{}])[0].get("Groups", []):
            cost = float(g["Metrics"]["UnblendedCost"]["Amount"])
            if cost > 0.01:
                services.append({"service": g["Keys"][0], "monthly_cost": round(cost, 2)})
        return sorted(services, key=lambda x: -x["monthly_cost"])
    except (ClientError, NoCredentialsError) as e:
        return [{"_error": str(e)[:200]}]
    except Exception as e:
        return [{"_error": str(e)[:200]}]


def get_tool_instances(session, region="us-east-1"):
    try:
        ec2 = session.client("ec2", region_name=region)
        instances = []
        for page in ec2.get_paginator("describe_instances").paginate():
            for res in page["Reservations"]:
                for i in res["Instances"]:
                    name = next((t["Value"] for t in i.get("Tags", []) if t["Key"] == "Name"), "")
                    instances.append({
                        "id": i["InstanceId"], "type": i["InstanceType"],
                        "state": i["State"]["Name"], "name": name,
                    })
        mapped = {}
        for inst in instances:
            nl = inst["name"].lower()
            for tool, patterns in TOOL_PATTERNS.items():
                if any(p in nl for p in patterns):
                    mapped.setdefault(tool, []).append(inst)
                    break
        return mapped
    except Exception as e:
        return {"_error": str(e)[:200]}


if __name__ == "__main__":
    os.makedirs("inventory/aws", exist_ok=True)
    profiles = get_profiles()
    print(f"Found {len(profiles)} mm-* profiles")

    results = {}
    for profile in profiles:
        print(f"\n=== {profile} ===")
        try:
            session = boto3.Session(profile_name=profile)
            ident = session.client("sts").get_caller_identity()
            account_id = ident["Account"]

            services = get_cost_by_service(session)
            tool_map = get_tool_instances(session)

            results[profile] = {
                "account_id": account_id,
                "cost_by_service": services,
                "tool_instances": tool_map if not isinstance(tool_map, dict) or "_error" not in tool_map else tool_map,
            }

            if services and "_error" not in services[0]:
                total = sum(s["monthly_cost"] for s in services)
                print(f"  ${total:,.2f}/month ({len(services)} services)")
                for s in services[:5]:
                    print(f"    {s['service']}: ${s['monthly_cost']:,.2f}")
            else:
                print(f"  Cost: {services}")

            if isinstance(tool_map, dict) and "_error" not in tool_map:
                for tool, insts in tool_map.items():
                    print(f"  Tool: {tool} -> {[i['name'] for i in insts]}")
        except Exception as e:
            results[profile] = {"_error": str(e)[:200]}
            print(f"  Error: {str(e)[:100]}")

    with open("inventory/aws/tool_cost_attribution.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nOutput: inventory/aws/tool_cost_attribution.json")
