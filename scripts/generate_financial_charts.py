"""Generate ECharts JSON for the Financial Intelligence minisite page.

Reads from analysis/ CSVs and inventory JSON, writes to analysis/charts/.
"""

import csv
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import tl_echarts_style as zcs

OUT = "analysis/charts"


def _read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def revenue_stacked_bar():
    rows = _read_csv("analysis/revenue_by_product.csv")
    quarters = [r["quarter"] for r in rows]
    series = [
        {"text": "Net Payments", "values": [int(r["net_payments"]) for r in rows]},
        {"text": "CAKE SaaS", "values": [int(r["cake_saas"]) for r in rows]},
        {"text": "Retail", "values": [int(r["retail"]) for r in rows]},
        {"text": "Other / Parafin", "values": [int(r["other_parafin"]) for r in rows]},
    ]
    config = zcs.bar_config(
        quarters, series,
        stacked=True,
        title="Revenue by Product Line",
        source="Cash Forecast Model",
        y_title="$USD",
    )
    zcs.add_source_annotation(config, "MS Cash Forecast")
    zcs.write_echarts_json(config, f"{OUT}/revenue_by_product_stacked.json")


def cash_flow_waterfall():
    rows = _read_csv("analysis/cash_flow_quarterly.csv")
    categories = []
    values = []
    for r in rows:
        q = r["quarter"]
        beginning = int(r["cash_beginning"])
        inflows = int(r["operating_inflows"])
        outflows = int(r["operating_outflows"])
        debt = int(r["debt_service"])
        infusion = int(r.get("cash_infusion", "0") or "0")

        categories.append(f"{q} Beginning")
        values.append(beginning)
        categories.append(f"{q} Inflows")
        values.append(inflows)
        categories.append(f"{q} Outflows")
        values.append(outflows)
        categories.append(f"{q} Debt")
        values.append(debt)
        if infusion:
            categories.append(f"{q} Infusion")
            values.append(infusion)
        categories.append(f"{q} Ending")
        values.append(int(r["cash_ending"]))

    config = zcs.waterfall_config(
        categories, values,
        title="Cash Flow Waterfall — Q1–Q4 2026",
        source="Cash Forecast Model",
    )
    zcs.add_source_annotation(config, "MS Cash Forecast")
    zcs.write_echarts_json(config, f"{OUT}/cash_flow_waterfall.json")


def vendor_spend_treemap():
    with open("inventory/vendor_spend_from_ap.json") as f:
        data = json.load(f)

    children = []
    for v in data.get("vendors", []):
        ann = v.get("annualized_est", 0)
        if ann > 0:
            children.append({
                "name": v["name"],
                "value": ann,
                "category": v.get("category", "Other"),
            })

    by_cat = {}
    for c in children:
        cat = c["category"]
        by_cat.setdefault(cat, []).append({"name": c["name"], "value": c["value"]})

    tree_data = [{"name": cat, "children": items} for cat, items in by_cat.items()]

    config = zcs.treemap_config(
        tree_data,
        title="Vendor Spend by Category",
        source="AP Aging Report",
    )
    zcs.add_source_annotation(config, "AP 03.30.26")
    zcs.write_echarts_json(config, f"{OUT}/vendor_spend_treemap.json")


def risk_bubble():
    with open("analysis/key_risks.json") as f:
        data = json.load(f)

    likelihood_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    impact_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

    points = []
    for r in data.get("risks", []):
        x = likelihood_map.get(r["likelihood"], 1)
        y = impact_map.get(r["impact"], 1)
        points.append([x, y, x * y, r["risk"]])

    series_data = [{
        "text": "Risks",
        "points": points,
    }]

    config = zcs.bubble_config(
        series_data,
        title="Risk Likelihood vs Impact",
        source="90-Day Plan",
        x_title="Likelihood",
        y_title="Impact",
    )

    for ax_key in ("xAxis", "yAxis"):
        ax = config.get(ax_key, {})
        ax["min"] = 0.5
        ax_map = likelihood_map if ax_key == "xAxis" else impact_map
        ax["max"] = max(ax_map.values()) + 0.5
        ax["axisLabel"] = {
            "formatter": None,
            "fontFamily": "Noto Sans Mono",
            "fontSize": 10,
        }

    config["xAxis"]["axisLabel"] = {
        "fontFamily": "Noto Sans Mono",
        "fontSize": 10,
    }
    config["yAxis"]["axisLabel"] = {
        "fontFamily": "Noto Sans Mono",
        "fontSize": 10,
    }

    zcs.add_source_annotation(config, "MadMobile 90-Day Plan")
    zcs.write_echarts_json(config, f"{OUT}/risk_likelihood_impact.json")


def cost_reduction_waterfall():
    with open("analysis/cost_reduction_targets.json") as f:
        data = json.load(f)

    items = data.get("items", [])
    categories = [i["action"] for i in items]
    values = [i["monthly_impact"] for i in items]

    config = zcs.waterfall_config(
        categories, values,
        title="Monthly Cost Reduction Breakdown",
        source="90-Day Plan",
    )
    zcs.add_source_annotation(config, "MS Cash Forecast / 90-Day Plan")
    zcs.write_echarts_json(config, f"{OUT}/cost_reduction_waterfall.json")


def retail_concentration_bar():
    rows = _read_csv("analysis/retail_client_revenue.csv")
    sorted_rows = sorted(rows, key=lambda r: int(r["total_52wk"]), reverse=True)
    categories = [r["client"] for r in sorted_rows]
    values = [int(r["total_52wk"]) for r in sorted_rows]

    config = zcs.bar_config(
        categories,
        [{"text": "52-Week Revenue", "values": values}],
        horizontal=True,
        title="Retail Client Concentration",
        source="Revenue Forecast",
        x_title="$USD",
    )
    zcs.add_source_annotation(config, "Retail Revenue Forecast")
    zcs.write_echarts_json(config, f"{OUT}/retail_concentration_bar.json")


if __name__ == "__main__":
    revenue_stacked_bar()
    cash_flow_waterfall()
    vendor_spend_treemap()
    risk_bubble()
    cost_reduction_waterfall()
    retail_concentration_bar()
    print("Generated 6 financial charts")
