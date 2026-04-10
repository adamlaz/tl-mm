"""Generate ECharts JSON for Executive RCA analysis charts."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import tl_echarts_style as zcs

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "analysis", "charts")


def executive_timeline():
    """Chart A: Horizontal bar showing 5 executive RCA incidents with duration."""
    option = zcs._base_option(
        title="Executive RCA Incidents — Last 90 Days",
        subtitle="Source: Executive RCAs from Chathura, April 2026"
    )
    zcs._apply_anim(option, "bar")

    incidents = [
        "Toastique OLO\n(Mar 20–23)",
        "Fish Seafood POS\n(Mar 14–15)",
        "Multi-System Outage\n(Feb 27)",
        "Sea Grill POS\n(Feb 8–19)",
        "Admin Portal\n(Dec 19)",
    ]

    durations_hours = [72, 17, 1.6, 288, 0.7]

    colors = [
        zcs.TL_CATEGORICAL[2],  # Amber — config
        zcs.TL_CATEGORICAL[3],  # Rose — merchant, Code Blue
        zcs.TL_CATEGORICAL[3],  # Rose — platform-wide
        zcs.TL_CATEGORICAL[2],  # Amber — merchant
        zcs.TL_CATEGORICAL[0],  # Indigo — platform-wide
    ]

    option["yAxis"] = {
        "type": "category",
        "data": incidents,
        "axisLabel": {
            "fontFamily": "Noto Sans",
            "fontSize": 10,
            "color": zcs.TL_LIGHT["text_muted"],
        },
        "axisLine": {"lineStyle": {"color": zcs.TL_LIGHT["zeroline"]}},
        "axisTick": {"show": False},
        "splitLine": {"show": False},
    }
    option["xAxis"] = zcs._val_axis(name="Duration (hours)")
    option["xAxis"]["type"] = "log"
    option["xAxis"]["min"] = 0.5
    option["xAxis"]["axisLabel"]["formatter"] = "{value}h"
    option["grid"] = {"containLabel": True, "left": 16, "right": 40, "top": 56, "bottom": 48}
    option["tooltip"]["trigger"] = "item"
    option["tooltip"]["formatter"] = "{b}: {c} hours"

    option["series"] = [{
        "type": "bar",
        "data": [
            {"value": d, "itemStyle": {"color": c}, "label": {"show": True, "position": "right", "fontFamily": "Noto Sans Mono", "fontSize": 10, "color": zcs.TL_LIGHT["text_secondary"], "formatter": f"{d}h" if d >= 1 else f"{int(d*60)}m"}}
            for d, c in zip(durations_hours, colors)
        ],
        "barWidth": "50%",
        "animationDuration": 600,
        "animationEasing": "quartOut",
    }]

    option["graphic"] = [
        {"type": "text", "left": "75%", "top": 58, "style": {"text": "Code Red", "fill": zcs.TL_STATUS["red"], "fontFamily": "Noto Sans", "fontSize": 9, "fontWeight": 600}},
        {"type": "text", "left": "60%", "top": 80, "style": {"text": "Code Blue", "fill": zcs.TL_STATUS["red"], "fontFamily": "Noto Sans", "fontSize": 9, "fontWeight": 600}},
        {"type": "text", "left": "75%", "top": 100, "style": {"text": "80 walkouts", "fill": zcs.TL_STATUS["amber"], "fontFamily": "Noto Sans", "fontSize": 9, "fontWeight": 600}},
    ]

    del option["legend"]
    zcs.write_echarts_json(option, os.path.join(CHARTS_DIR, "rca_executive_timeline.json"))
    print("  rca_executive_timeline.json")


def failure_classes():
    """Chart B: Grouped bar — recurring failure classes, historical vs recent."""
    option = zcs._base_option(
        title="Recurring Failure Classes — 2020–2026",
        subtitle="Source: Confluence RCAs + Executive RCAs, April 2026"
    )
    zcs._apply_anim(option, "bar")

    categories = [
        "ESB / DB\nOverload",
        "CouchDB\nCorruption",
        "Certificate\nExpiry",
        "Config /\nOnboarding",
        "Payment\nProvider",
        "Report\nSync",
    ]

    option["xAxis"] = zcs._cat_axis(categories)
    option["yAxis"] = zcs._val_axis(name="Incidents")
    option["grid"] = {"containLabel": True, "left": 16, "right": 16, "top": 56, "bottom": 72}

    option["series"] = [
        {
            "name": "Confluence RCAs (2020–2025)",
            "type": "bar",
            "data": [6, 3, 1, 2, 7, 4],
            "itemStyle": {"color": zcs.TL_CATEGORICAL[4]},
            "animationDelay": 0,
        },
        {
            "name": "Executive RCAs (Dec 2025–Mar 2026)",
            "type": "bar",
            "data": [2, 2, 1, 1, 0, 0],
            "itemStyle": {"color": zcs.TL_CATEGORICAL[3]},
            "animationDelay": 120,
        },
    ]

    option["legend"]["data"] = ["Confluence RCAs (2020–2025)", "Executive RCAs (Dec 2025–Mar 2026)"]

    zcs.write_echarts_json(option, os.path.join(CHARTS_DIR, "rca_failure_classes.json"))
    print("  rca_failure_classes.json")


def preventive_actions():
    """Chart C: Stacked bar — preventive action completion across RCAs."""
    option = zcs._base_option(
        title="Preventive Action Follow-Through — 55 RCAs",
        subtitle="Source: Confluence + Executive RCAs, April 2026"
    )
    zcs._apply_anim(option, "bar")

    categories = ["Confluence\n2020–2023\n(48 RCAs)", "Executive\nDec 2025–\nMar 2026\n(5 RCAs)", "Team Tesla\n2025\n(2 RCAs)"]

    option["xAxis"] = zcs._cat_axis(categories)
    option["yAxis"] = zcs._val_axis(name="RCA Documents")
    option["grid"] = {"containLabel": True, "left": 16, "right": 16, "top": 56, "bottom": 72}

    option["series"] = [
        {
            "name": "Empty / No Actions",
            "type": "bar",
            "stack": "total",
            "data": [30, 3, 0],
            "itemStyle": {"color": zcs.TL_STATUS["red"]},
        },
        {
            "name": "Planned / In Progress",
            "type": "bar",
            "stack": "total",
            "data": [12, 2, 1],
            "itemStyle": {"color": zcs.TL_STATUS["amber"]},
        },
        {
            "name": "Completed",
            "type": "bar",
            "stack": "total",
            "data": [6, 0, 1],
            "itemStyle": {"color": zcs.TL_STATUS["green"]},
        },
    ]

    option["legend"]["data"] = ["Empty / No Actions", "Planned / In Progress", "Completed"]

    zcs.write_echarts_json(option, os.path.join(CHARTS_DIR, "rca_preventive_actions.json"))
    print("  rca_preventive_actions.json")


def update_timeline():
    """Update the existing confluence_rca_timeline.json with 2026 data."""
    import json
    path = os.path.join(CHARTS_DIR, "confluence_rca_timeline.json")
    with open(path) as f:
        chart = json.load(f)

    opt = chart["option"]
    opt["title"]["text"] = "RCA Incident Frequency — 55 Total (incl. 5 Executive RCAs)"
    opt["xAxis"]["data"].append("2026")
    opt["series"][0]["data"].append(5)

    with open(path, "w") as f:
        json.dump(chart, f, ensure_ascii=False, separators=(",", ":"))
    print("  confluence_rca_timeline.json (updated)")


if __name__ == "__main__":
    print("Generating RCA charts...")
    update_timeline()
    executive_timeline()
    failure_classes()
    preventive_actions()
    print("Done.")
