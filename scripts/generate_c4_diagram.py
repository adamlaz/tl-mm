#!/usr/bin/env python3
"""Generate D2 C4 diagrams (context + container) from AWS inventory data.

Outputs MDX files for the astro-d2 integration and raw .d2 source files.
"""

import json
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUTS = {
    "route53": os.path.join(BASE, "inventory", "aws", "route53_zones.json"),
    "ecs_services": os.path.join(BASE, "inventory", "aws", "ecs_services.json"),
    "ecs_tasks": os.path.join(BASE, "inventory", "aws", "ecs_task_definitions.json"),
    "eks": os.path.join(BASE, "inventory", "aws", "eks_clusters.json"),
    "prod_us": os.path.join(BASE, "inventory", "aws", "mm-retail-prod-us.json"),
}

OUT_MDX_CONTEXT = os.path.join(BASE, "minisite", "src", "diagrams", "c4-context.mdx")
OUT_MDX_CONTAINER = os.path.join(BASE, "minisite", "src", "diagrams", "c4-container.mdx")
OUT_D2_CONTEXT = os.path.join(BASE, "analysis", "diagrams", "c4_context.d2")
OUT_D2_CONTAINER = os.path.join(BASE, "analysis", "diagrams", "c4_container.d2")

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

DOMAIN_FILLS = {
    "payments": "#FCE7EC",
    "cake_pos": "#F5F0E6",
    "concierge": "#E0E7FF",
    "platform": "#E8ECF0",
    "api_gateway": "#D4E7D0",
    "neo_ai": "#F0E7F0",
    "analytics": "#E8F0E0",
    "customer_engagement": "#FFF0E0",
    "workforce": "#E0E7FF",
    "hardware_integration": "#D4E7D0",
    "notifications": "#F5F0E6",
    "observability": "#FCE7EC",
}


def load(key):
    with open(INPUTS[key]) as f:
        return json.load(f)


def d2_id(name: str) -> str:
    """Sanitize a name into a valid D2 identifier."""
    s = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if s and s[0].isdigit():
        s = "_" + s
    return s


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


# ---------------------------------------------------------------------------
# D2 builders
# ---------------------------------------------------------------------------

def build_context_d2(customers, domain_counts, route53_zones) -> str:
    """Build D2 source for the C4 system context diagram."""
    domain_names = [z["name"].rstrip(".") for z in route53_zones]
    brands = ", ".join(customers[:6]) + ("..." if len(customers) > 6 else "")
    lines: list[str] = []

    lines.append("direction: down")
    lines.append("")
    lines.append("# Source: AWS Inventory, extracted April 2026")
    lines.append("")

    # --- External actors ---
    lines.append("external_actors: External Actors {")
    lines.append('  style.fill: "#E0E7FF"')
    lines.append("")
    lines.append("  retail_customers: Retail Customers {")
    lines.append("    shape: person")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append(f"  retail_brands: Retail Brands\\n{brands} {{")
    lines.append("    shape: person")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append("  sysco: Sysco / Restaurant Chains {")
    lines.append("    shape: person")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append("  payment_processors: Payment Processors\\nAurus, RS2 Bankworks {")
    lines.append("    shape: person")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append("  apple_bestbuy: Apple / Best Buy {")
    lines.append("    shape: person")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append("}")
    lines.append("")

    # --- Mad Mobile Platform ---
    lines.append("platform: Mad Mobile Platform {")
    lines.append('  style.fill: "#DCFCE7"')
    lines.append('  style.stroke: "#2A9D8F"')
    lines.append("")
    lines.append("  cake: CAKE POS {")
    lines.append('    style.fill: "#F5F0E6"')
    lines.append("  }")
    lines.append("  concierge: Concierge {")
    lines.append('    style.fill: "#E0E7FF"')
    lines.append("  }")
    lines.append("  payments: Mad Payments {")
    lines.append('    style.fill: "#FCE7EC"')
    lines.append("  }")
    lines.append("  neo_ai: Neo AI / Marvel Cloud {")
    lines.append('    style.fill: "#F0E7F0"')
    lines.append("  }")
    lines.append("  platform_svc: Platform Services {")
    lines.append('    style.fill: "#E8ECF0"')
    lines.append("  }")
    lines.append("}")
    lines.append("")

    # --- Infrastructure ---
    lines.append("infra: Infrastructure {")
    lines.append('  style.fill: "#E8F5E0"')
    lines.append("")
    lines.append("  aws: AWS\\nECS, EKS, DynamoDB, S3, Lambda {")
    lines.append('    style.fill: "#E8F5E0"')
    lines.append("  }")
    lines.append("  monitoring: Monitoring\\nPrometheus, OpenTelemetry {")
    lines.append('    style.fill: "#E8F5E0"')
    lines.append("  }")
    lines.append("  cicd: CI/CD\\nBitbucket Pipelines, CodePipeline {")
    lines.append('    style.fill: "#E8F5E0"')
    lines.append("  }")
    lines.append("}")
    lines.append("")

    # --- DNS ---
    zone_count = len(domain_names)
    lines.append(f"dns: DNS / Domains ({zone_count}) {{")
    lines.append('  style.fill: "#F0E7F0"')
    lines.append("")
    for dn in domain_names[:10]:
        lines.append(f"  {d2_id(dn)}: {dn}")
    if zone_count > 10:
        lines.append(f"  more: +{zone_count - 10} more")
    lines.append("}")
    lines.append("")

    # --- Relationships ---
    lines.append("# Relationships")
    lines.append('external_actors.retail_customers -> platform.cake: "POS & ordering"')
    lines.append('external_actors.retail_customers -> platform.concierge: "clienteling"')
    lines.append('external_actors.retail_brands -> platform.concierge: "analytics"')
    lines.append('external_actors.sysco -> platform.cake: "CAKE POS"')
    lines.append('external_actors.payment_processors -> platform.payments: "card processing"')
    lines.append('external_actors.apple_bestbuy -> platform.concierge: "concierge deployments"')
    lines.append("")
    lines.append('platform -> infra.aws: "runs on"')
    lines.append('platform -> infra.monitoring: "observability"')
    lines.append('platform -> infra.cicd: "deployments"')
    lines.append('platform -> dns: "serves"')

    return "\n".join(lines) + "\n"


def build_container_d2(ecs_data) -> str:
    """Build D2 source for the C4 container diagram."""
    domain_services: dict[str, dict[str, dict]] = defaultdict(dict)

    for cluster_info in ecs_data.values():
        for svc in cluster_info.get("services", []):
            domain = categorize_ecs_service(svc["name"])
            if not domain:
                continue
            name = svc["name"]
            running = svc.get("running", 0)
            desired = svc.get("desired", 0)
            if name in domain_services[domain]:
                prev = domain_services[domain][name]
                prev["running"] = max(prev["running"], running)
                prev["desired"] = max(prev["desired"], desired)
            else:
                domain_services[domain][name] = {
                    "name": name, "running": running, "desired": desired,
                }

    lines: list[str] = []
    lines.append("direction: right")
    lines.append("")
    lines.append("# Source: AWS Inventory, extracted April 2026")
    lines.append("")

    for domain_key, label in DOMAIN_LABELS.items():
        services = sorted(domain_services.get(domain_key, {}).values(), key=lambda s: s["name"])
        fill = DOMAIN_FILLS[domain_key]
        container_id = d2_id(domain_key)
        count = len(services)

        lines.append(f"{container_id}: {label} ({count} services) {{")
        lines.append(f'  style.fill: "{fill}"')
        lines.append("")

        for svc in services:
            sid = d2_id(svc["name"])
            status = "running" if svc["running"] > 0 else "stopped"
            svc_label = f'{svc["name"]}\\n{status} ({svc["running"]}/{svc["desired"]})'
            lines.append(f"  {sid}: {svc_label}")

        lines.append("}")
        lines.append("")

    # --- Inter-domain relationships ---
    lines.append("# Inter-domain relationships")
    has = {k for k, v in domain_services.items() if v}
    rels = [
        ("cake_pos", "payments", "payment processing"),
        ("cake_pos", "api_gateway", "API routing"),
        ("concierge", "api_gateway", "API routing"),
        ("concierge", "analytics", "reporting"),
        ("payments", "notifications", "alerts"),
        ("platform", "api_gateway", "gateway config"),
        ("platform", "notifications", "system notifications"),
        ("platform", "observability", "monitoring"),
        ("neo_ai", "platform", "platform APIs"),
        ("customer_engagement", "notifications", "marketing"),
        ("workforce", "platform", "platform APIs"),
    ]
    for src, dst, lbl in rels:
        if src in has and dst in has:
            lines.append(f'{d2_id(src)} -> {d2_id(dst)}: "{lbl}"')

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def wrap_mdx(d2_source: str, title: str, width: int = 900) -> str:
    return f'```d2 title="{title}" width={width}\n{d2_source}```\n'


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== C4 Diagrams (D2) ===", flush=True)

    route53 = load("route53")
    ecs_data = load("ecs_services")
    prod_data = load("prod_us")

    customers = extract_s3_customers(prod_data)
    print(f"  Found {len(customers)} customer brands from S3 buckets")

    domain_counts = defaultdict(int)
    for cluster_info in ecs_data.values():
        for svc in cluster_info.get("services", []):
            domain = categorize_ecs_service(svc["name"])
            if domain:
                domain_counts[domain] += 1
    print("  Categorized ECS services by domain:")
    for dom, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"    {DOMAIN_LABELS.get(dom, dom)}: {c} services")

    # Context diagram
    ctx_d2 = build_context_d2(customers, domain_counts, route53)
    write(OUT_D2_CONTEXT, ctx_d2)
    print(f"\n  Wrote {OUT_D2_CONTEXT}")

    ctx_mdx = wrap_mdx(ctx_d2, "C4 System Context — Mad Mobile")
    write(OUT_MDX_CONTEXT, ctx_mdx)
    print(f"  Wrote {OUT_MDX_CONTEXT}")

    # Container diagram
    ctr_d2 = build_container_d2(ecs_data)
    write(OUT_D2_CONTAINER, ctr_d2)
    print(f"\n  Wrote {OUT_D2_CONTAINER}")

    ctr_mdx = wrap_mdx(ctr_d2, "C4 Container Diagram — Mad Mobile Platform")
    write(OUT_MDX_CONTAINER, ctr_mdx)
    print(f"  Wrote {OUT_MDX_CONTAINER}")

    print(f"\n  Customers ({len(customers)}): {', '.join(customers[:12])}...")
    print(f"  Route53 zones: {len(route53)}")
    print(f"  ECS clusters: {len(ecs_data)}")


if __name__ == "__main__":
    main()
