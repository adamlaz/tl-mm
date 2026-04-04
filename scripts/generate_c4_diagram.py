#!/usr/bin/env python3
"""Generate Mermaid C4 Context and Container diagrams from AWS inventory data."""

import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUTS = {
    "route53": os.path.join(BASE, "inventory", "aws", "route53_zones.json"),
    "ecs_services": os.path.join(BASE, "inventory", "aws", "ecs_services.json"),
    "ecs_tasks": os.path.join(BASE, "inventory", "aws", "ecs_task_definitions.json"),
    "eks": os.path.join(BASE, "inventory", "aws", "eks_clusters.json"),
    "prod_us": os.path.join(BASE, "inventory", "aws", "mm-retail-prod-us.json"),
}

OUT_CONTEXT = os.path.join(BASE, "inventory", "mad-mobile-c4-context.mmd")
OUT_CONTAINER = os.path.join(BASE, "inventory", "mad-mobile-c4-container.mmd")


def load(key):
    with open(INPUTS[key]) as f:
        return json.load(f)


def categorize_ecs_service(name: str) -> str | None:
    """Map an ECS service name to a Mad Mobile product domain."""
    n = name.lower().replace("-", "_").replace(" ", "_")
    if any(k in n for k in ["payment", "merchant", "emaf", "petl", "pac_", "echeck", "chargeback"]):
        return "payments"
    if any(k in n for k in ["menu", "daypart", "order", "kitchen", "kds", "modifier"]):
        return "cake_pos"
    if any(k in n for k in ["concierge", "clienteling", "curbside", "appointment"]):
        return "concierge"
    if any(k in n for k in ["config", "operator", "admin", "onboarding", "template"]):
        return "platform"
    if any(k in n for k in ["janus", "gateway", "tyk", "api_gateway", "redirector"]):
        return "api_gateway"
    if any(k in n for k in ["neo", "ai", "assistant", "marvel"]):
        return "neo_ai"
    if any(k in n for k in ["report", "analytic", "accounting"]):
        return "analytics"
    if any(k in n for k in ["wallet", "loyalty", "customer_profile", "marketing"]):
        return "customer_engagement"
    if any(k in n for k in ["staff", "timesheet", "jobassign", "payroll", "schedule"]):
        return "workforce"
    if any(k in n for k in ["printer", "peripheral", "beacon"]):
        return "hardware_integration"
    if any(k in n for k in ["email", "notification"]):
        return "notifications"
    if any(k in n for k in ["otel", "monitoring"]):
        return "observability"
    return None


DOMAIN_LABELS = {
    "payments": "Mad Payments",
    "cake_pos": "CAKE POS Core",
    "concierge": "Concierge (Clienteling)",
    "platform": "Platform Services",
    "api_gateway": "API Gateway",
    "neo_ai": "Neo AI / Marvel Cloud",
    "analytics": "Analytics & Reporting",
    "customer_engagement": "Customer Engagement",
    "workforce": "Workforce Management",
    "hardware_integration": "Hardware Integration",
    "notifications": "Notifications",
    "observability": "Observability",
}


def extract_s3_customers(prod_data: dict) -> list[str]:
    """Pull customer names from S3 analytics/concierge buckets."""
    customers = set()
    for region_data in prod_data.get("regions", {}).values():
        for bucket in region_data.get("s3_buckets", []):
            name = bucket["name"]
            for prefix in ("concierge-analytics-", "cake-analytics-"):
                if name.startswith(prefix):
                    cust = name[len(prefix):].replace("-", " ").title()
                    if cust and cust not in ("Domo", "Madmobile", "S3"):
                        customers.add(cust)
    return sorted(customers)


def generate_context_diagram(customers: list[str], domains: dict, route53_zones: list) -> str:
    """Generate C4 Context level diagram."""
    domain_names = [z["name"].rstrip(".") for z in route53_zones]

    lines = [
        "---",
        "title: Mad Mobile - C4 Context Diagram",
        "---",
        "flowchart TB",
        "",
        "    %% External Actors",
        '    Customers["🏪 Retail Customers<br/><i>POS, ordering, payments</i>"]',
        '    Retailers["🏬 Retail Brands<br/><i>' + ", ".join(customers[:8]) + '...</i>"]',
        '    Sysco["🍽️ Sysco / Restaurant Chains<br/><i>CAKE POS deployments</i>"]',
        '    PayProc["💳 Payment Processors<br/><i>Aurus, RS2 Bankworks,<br/>Card Networks</i>"]',
        '    AppleBB["📱 Apple / Best Buy<br/><i>Concierge deployments</i>"]',
        "",
        "    %% Mad Mobile Systems",
        '    subgraph MM["<b>Mad Mobile Platform</b>"]',
        '        direction TB',
        '        CAKE["🍰 CAKE POS<br/><i>Restaurant POS, Menu Mgmt,<br/>Kitchen Display, Orders</i>"]',
        '        CONC["👔 Concierge<br/><i>Clienteling, Appointments,<br/>Curbside, Analytics</i>"]',
        '        PAY["💰 Mad Payments<br/><i>Payment Gateway, Merchant<br/>Onboarding, Chargeback</i>"]',
        '        NEO["🤖 Neo AI / Marvel Cloud<br/><i>AI Assistant, Data Platform</i>"]',
        '        PLAT["⚙️ Platform Services<br/><i>Config, Admin, API Gateway,<br/>Notifications</i>"]',
        "    end",
        "",
        "    %% Internal Systems",
        '    subgraph INFRA["<b>Infrastructure</b>"]',
        '        direction TB',
        '        AWS["☁️ AWS<br/><i>ECS, EKS, DynamoDB,<br/>S3, Lambda, ElastiCache</i>"]',
        '        MON["📊 Monitoring<br/><i>Prometheus, Elasticsearch,<br/>OpenTelemetry, CloudWatch</i>"]',
        '        CICD["🔧 CI/CD<br/><i>Bitbucket Pipelines,<br/>GitOps, CodePipeline</i>"]',
        "    end",
        "",
        "    %% DNS",
        '    subgraph DNS["<b>DNS / Domains</b>"]',
        '        direction LR',
    ]
    for d in domain_names:
        safe_id = d.replace(".", "_").replace("-", "_")
        lines.append(f'        {safe_id}["{d}"]')
    lines += [
        "    end",
        "",
        "    %% Relationships",
        "    Customers --> CAKE",
        "    Customers --> CONC",
        "    Customers --> PAY",
        "    Retailers --> CONC",
        "    Sysco --> CAKE",
        "    AppleBB --> CONC",
        "    PayProc <--> PAY",
        "    CAKE --> PAY",
        "    CONC --> PAY",
        "    CAKE --> PLAT",
        "    CONC --> PLAT",
        "    PAY --> PLAT",
        "    NEO --> PLAT",
        "    MM --> INFRA",
        "    MM --> DNS",
        "",
        '    %% Styling',
        '    classDef external fill:#DBEAFE,stroke:#3B82F6,color:#1E40AF',
        '    classDef mmSystem fill:#DCFCE7,stroke:#22C55E,color:#166534',
        '    classDef infra fill:#FEF3C7,stroke:#F59E0B,color:#92400E',
        '    class Customers,Retailers,Sysco,PayProc,AppleBB external',
        '    class CAKE,CONC,PAY,NEO,PLAT mmSystem',
        '    class AWS,MON,CICD infra',
    ]
    return "\n".join(lines)


def generate_container_diagram(ecs_data: dict, ecs_tasks: dict, eks_data: list, prod_data: dict) -> str:
    """Generate C4 Container level diagram from ECS/EKS inventory."""

    # gather prod ECS services by domain
    domain_services: dict[str, list[dict]] = defaultdict(list)
    all_services_flat = []

    for cluster_key, cluster_info in ecs_data.items():
        profile = cluster_info["profile"]
        cluster = cluster_info["cluster"]
        for svc in cluster_info.get("services", []):
            domain = categorize_ecs_service(svc["name"])
            entry = {
                "name": svc["name"],
                "cluster": cluster,
                "profile": profile,
                "running": svc.get("running", 0),
                "desired": svc.get("desired", 0),
                "launch_type": svc.get("launch_type", "?"),
            }
            all_services_flat.append(entry)
            if domain:
                domain_services[domain].append(entry)

    # prod ECS task definitions with images
    prod_images = defaultdict(set)
    for task in ecs_tasks.get("services", []):
        domain = categorize_ecs_service(task.get("service", ""))
        if domain:
            for c in task.get("containers", []):
                img = c.get("image", "")
                short_img = img.split("/")[-1].split(":")[0] if "/" in img else img.split(":")[0]
                if short_img and short_img != "nginx":
                    prod_images[domain].add(short_img)

    # EKS clusters
    eks_clusters_info = []
    for cl in eks_data:
        node_count = sum(ng.get("desired_size", 0) for ng in cl.get("node_groups", []))
        eks_clusters_info.append({
            "name": cl["name"],
            "version": cl.get("k8s_version", "?"),
            "nodes": node_count,
            "profile": cl.get("profile", ""),
        })

    # DynamoDB tables from prod
    dynamo_tables = []
    for region_data in prod_data.get("regions", {}).values():
        dynamo_tables.extend(region_data.get("dynamodb_tables", []))

    # Lambda functions
    lambda_functions = []
    for region_data in prod_data.get("regions", {}).values():
        lambda_functions.extend(region_data.get("lambda_functions", []))

    lines = [
        "---",
        "title: Mad Mobile - C4 Container Diagram",
        "---",
        "flowchart TB",
        "",
    ]

    # CAKE POS subsystem
    cake_svcs = domain_services.get("cake_pos", [])
    running_cake = [s for s in cake_svcs if s["running"] > 0]
    lines += [
        '    subgraph CAKE["🍰 <b>CAKE POS</b>"]',
        '        direction TB',
        f'        CAKE_MENU["Menu API<br/><i>{len([s for s in cake_svcs if "menu" in s["name"].lower()])} services</i>"]',
        f'        CAKE_ORDER["Order Management<br/><i>order-proxy, order-api</i>"]',
        f'        CAKE_KDS["Kitchen Display<br/><i>KDS, daypart, modifiers</i>"]',
        f'        CAKE_ADMIN["Restaurant Admin<br/><i>admin portal v2</i>"]',
        '    end',
        '',
    ]

    # Concierge subsystem
    conc_svcs = domain_services.get("concierge", [])
    lines += [
        '    subgraph CONC["👔 <b>Concierge</b>"]',
        '        direction TB',
        '        CONC_CLIENT["Clienteling App<br/><i>concierge-associate</i>"]',
        '        CONC_CURB["Curbside Pickup<br/><i>microsites, webhooks</i>"]',
        f'        CONC_ANALYTICS["Analytics Engine<br/><i>{len([l for l in lambda_functions if "concierge_analytics" in l.get("name", "")])} Lambda functions</i>"]',
        '    end',
        '',
    ]

    # Payments subsystem
    pay_svcs = domain_services.get("payments", [])
    pay_names = sorted(set(s["name"].replace("_service", "").replace("src-", "").replace("pos4_", "") for s in pay_svcs))[:8]
    lines += [
        '    subgraph PAY["💰 <b>Mad Payments</b>"]',
        '        direction TB',
        '        PAY_GW["Payment Gateway<br/><i>cake-payment-gateway</i>"]',
        '        PAY_ADMIN["Payments Admin<br/><i>admin-api, config-portal</i>"]',
        '        PAY_ONBOARD["Merchant Onboarding<br/><i>onboarding-v3</i>"]',
        '        PAY_PROC["Processing<br/><i>PETL, EMAF, eCheck,<br/>chargeback</i>"]',
        '        PAY_PCC["Payment Control Center<br/><i>PCC dashboard</i>"]',
        '    end',
        '',
    ]

    # Neo AI / Marvel Cloud
    lines += [
        '    subgraph NEO["🤖 <b>Neo AI / Marvel Cloud</b>"]',
        '        direction TB',
    ]
    for cl in eks_clusters_info:
        safe = cl["name"].replace("-", "_")
        lines.append(
            f'        EKS_{safe}["EKS: {cl["name"]}<br/>'
            f'<i>k8s {cl["version"]}, {cl["nodes"]} nodes</i>"]'
        )
    lines += [
        '        NEO_AI["AI Assistant<br/><i>cake-ai-assistant-data</i>"]',
        '    end',
        '',
    ]

    # Platform Services
    plat_svcs = domain_services.get("platform", [])
    gw_svcs = domain_services.get("api_gateway", [])
    lines += [
        '    subgraph PLAT["⚙️ <b>Platform Services</b>"]',
        '        direction TB',
        '        PLAT_CONFIG["Config Server<br/><i>config-api</i>"]',
        f'        PLAT_GW["API Gateway<br/><i>Janus, Tyk<br/>{len(gw_svcs)} instances</i>"]',
        '        PLAT_ADMIN["Operator Admin<br/><i>operator-api, SCAT tool</i>"]',
        '        PLAT_NOTIF["Notifications<br/><i>email service</i>"]',
        '    end',
        '',
    ]

    # Infrastructure
    prod_clusters = set()
    for ck, ci in ecs_data.items():
        if "prod" in ci["profile"].lower() or "production" in ci["profile"].lower():
            prod_clusters.add(ci["cluster"])

    lines += [
        '    subgraph INFRA["☁️ <b>AWS Infrastructure</b>"]',
        '        direction TB',
    ]

    # ECS clusters
    env_clusters = defaultdict(int)
    for ck, ci in ecs_data.items():
        profile = ci["profile"]
        if "prod" in profile:
            env_clusters["production"] += ci["service_count"]
        elif "dev" in profile or "r-and-d" in profile:
            env_clusters["development"] += ci["service_count"]

    lines += [
        f'        ECS["ECS Clusters<br/><i>{len(ecs_data)} clusters<br/>'
        f'prod: {env_clusters.get("production", 0)} svcs, '
        f'dev: {env_clusters.get("development", 0)} svcs</i>"]',
    ]

    # DynamoDB
    if dynamo_tables:
        lines.append(
            f'        DYNAMO["DynamoDB<br/><i>{len(dynamo_tables)} tables<br/>'
            f'{", ".join(dynamo_tables[:4])}...</i>"]'
        )

    # S3
    s3_count = sum(
        len(rd.get("s3_buckets", []))
        for rd in prod_data.get("regions", {}).values()
    )
    lines.append(f'        S3["S3<br/><i>{s3_count} buckets (prod-us)</i>"]')

    # Lambda
    lines.append(f'        LAMBDA["Lambda<br/><i>{len(lambda_functions)} functions</i>"]')

    # Monitoring
    lines += [
        '        PROM["Prometheus + Elasticsearch<br/><i>prod-prometheus, prod-elasticsearch x3</i>"]',
        '        OTEL["OpenTelemetry Collector<br/><i>distributed tracing</i>"]',
    ]

    lines += ['    end', '']

    # Relationships
    lines += [
        "    %% Inter-system relationships",
        "    CAKE_ORDER --> PAY_GW",
        "    CAKE_MENU --> PLAT_CONFIG",
        "    CONC_CLIENT --> PAY_GW",
        "    CONC_ANALYTICS --> S3",
        "    CONC_ANALYTICS --> LAMBDA",
        "    PAY_GW --> PAY_PROC",
        "    PAY_ADMIN --> PAY_ONBOARD",
        "    PLAT_GW --> CAKE",
        "    PLAT_GW --> CONC",
        "    PLAT_GW --> PAY",
        "    NEO_AI --> S3",
    ]
    for cl in eks_clusters_info:
        safe = cl["name"].replace("-", "_")
        lines.append(f"    EKS_{safe} --> DYNAMO")

    lines += [
        "    CAKE --> ECS",
        "    PAY --> ECS",
        "    CONC --> ECS",
        "    PLAT --> ECS",
        "    INFRA --> PROM",
        "    INFRA --> OTEL",
        "",
        "    %% Styling",
        '    classDef cakeStyle fill:#FEF3C7,stroke:#F59E0B,color:#92400E',
        '    classDef concStyle fill:#DBEAFE,stroke:#3B82F6,color:#1E40AF',
        '    classDef payStyle fill:#FCE7F3,stroke:#EC4899,color:#9D174D',
        '    classDef neoStyle fill:#E0E7FF,stroke:#6366F1,color:#3730A3',
        '    classDef platStyle fill:#F3F4F6,stroke:#6B7280,color:#374151',
        '    classDef infraStyle fill:#DCFCE7,stroke:#22C55E,color:#166534',
        '    class CAKE_MENU,CAKE_ORDER,CAKE_KDS,CAKE_ADMIN cakeStyle',
        '    class CONC_CLIENT,CONC_CURB,CONC_ANALYTICS concStyle',
        '    class PAY_GW,PAY_ADMIN,PAY_ONBOARD,PAY_PROC,PAY_PCC payStyle',
    ]
    eks_classes = ",".join(f"EKS_{cl['name'].replace('-', '_')}" for cl in eks_clusters_info)
    lines.append(f'    class {eks_classes},NEO_AI neoStyle')
    lines += [
        '    class PLAT_CONFIG,PLAT_GW,PLAT_ADMIN,PLAT_NOTIF platStyle',
        '    class ECS,DYNAMO,S3,LAMBDA,PROM,OTEL infraStyle',
    ]

    return "\n".join(lines)


def main():
    route53 = load("route53")
    ecs_data = load("ecs_services")
    ecs_tasks = load("ecs_tasks")
    eks_data = load("eks")
    prod_data = load("prod_us")

    customers = extract_s3_customers(prod_data)
    print(f"  Found {len(customers)} customer brands from S3 buckets")

    # domain breakdown from ECS
    domain_counts = defaultdict(int)
    for cluster_info in ecs_data.values():
        for svc in cluster_info.get("services", []):
            domain = categorize_ecs_service(svc["name"])
            if domain:
                domain_counts[domain] += 1
    print(f"  Categorized ECS services by domain:")
    for d, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"    {DOMAIN_LABELS.get(d, d)}: {c} services")

    ctx = generate_context_diagram(customers, domain_counts, route53)
    with open(OUT_CONTEXT, "w") as f:
        f.write(ctx)
    print(f"\n  Wrote {OUT_CONTEXT}")

    container = generate_container_diagram(ecs_data, ecs_tasks, eks_data, prod_data)
    with open(OUT_CONTAINER, "w") as f:
        f.write(container)
    print(f"  Wrote {OUT_CONTAINER}")

    print(f"\n  Customers ({len(customers)}): {', '.join(customers[:12])}...")
    print(f"  EKS clusters: {len(eks_data)}")
    print(f"  ECS clusters: {len(ecs_data)}")
    print(f"  Route53 zones: {len(route53)}")


if __name__ == "__main__":
    main()
