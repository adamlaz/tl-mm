"""Translation Layer chart style system — Apache ECharts v6 edition.

TL brand tokens (Noto fonts, OKLCH-derived palettes, status colors).
Builder functions produce ECharts option dicts; write_echarts_json()
serializes them to JSON for inline rendering in the minisite.

Usage::

    import tl_echarts_style as zcs
    config = zcs.bar_config(["Q1","Q2","Q3"], [{"text":"Revenue","values":[10,20,30]}],
                            title="Revenue by Quarter", source="Jira")
    zcs.write_echarts_json(config, "analysis/charts/revenue.json")
"""

import json
import math
import os
import re

# ── Categorical palette (8 colors, max perceptual distance) ──────────────

TL_CATEGORICAL = [
    "#4A5FC4",  # Indigo
    "#2A9D8F",  # Teal
    "#C4973A",  # Amber
    "#C4574A",  # Rose
    "#6B82A0",  # Slate Blue
    "#6FAA5C",  # Olive
    "#9A6B9A",  # Mauve
    "#B07A4A",  # Sienna
]

TL_CATEGORICAL_DARK = [
    "#6B7FE0", "#3AC4B4", "#D4A74A", "#D46A5A",
    "#8A9EC0", "#8ACC7A", "#B48AB4", "#C89060",
]

# ── Sequential palette (warm, 6 stops) ──────────────────────────────────

TL_SEQUENTIAL = ["#F5F0E6", "#E0D0AA", "#C4A870", "#A08040", "#7A5E28", "#5A3E18"]
TL_SEQUENTIAL_DARK = ["#2A2420", "#4A3E28", "#7A6030", "#A08040", "#C4A060", "#E0C48A"]

# ── Diverging palette (positive/negative threshold) ─────────────────────

TL_DIVERGING = ["#B84030", "#D08060", "#F0E8DC", "#60C0A0", "#309878"]

# ── Status colors ───────────────────────────────────────────────────────

TL_STATUS = {
    "green": "#3AAA5C",
    "amber": "#C4973A",
    "red": "#CC4A3A",
    "green_bg": "#E8F5EC",
    "amber_bg": "#F5F0E6",
    "red_bg": "#F5E8E6",
}

# ── Surface tokens ──────────────────────────────────────────────────────

TL_LIGHT = {
    "bg": "#FFFFFF",
    "text": "#2E2820",
    "text_secondary": "#5A5048",
    "text_muted": "#8A8070",
    "grid": "#E8E4DE",
    "zeroline": "#D0C8BA",
    "border": "#E8E4DE",
    "surface": "#FFFFFF",
}

TL_DARK = {
    "bg": "#1E1A1A",
    "text": "#E8E4DE",
    "text_secondary": "#B0A890",
    "text_muted": "#8A8070",
    "grid": "#3A3430",
    "zeroline": "#4A4038",
    "border": "#4A4038",
    "surface": "#1E1A1A",
}

# ── Animation timing ────────────────────────────────────────────────────

_ANIM = {
    "bar":       {"duration": 600, "easing": "quartOut", "type": "scale"},
    "line":      {"duration": 800, "easing": "cubicOut", "type": "expansion"},
    "gauge":     {"duration": 1200, "easing": "elasticOut", "type": "scale"},
    "radar":     {"duration": 700, "easing": "quartOut", "type": "scale"},
    "chord":     {"duration": 1000, "easing": "quartOut", "type": "scale"},
    "heatmap":   {"duration": 800, "easing": "quartOut", "type": "scale"},
    "treemap":   {"duration": 700, "easing": "quartOut", "type": "scale"},
    "sunburst":  {"duration": 800, "easing": "quartOut", "type": "scale"},
    "funnel":    {"duration": 600, "easing": "quartOut", "type": "scale"},
    "scatter":   {"duration": 800, "easing": "quartOut", "type": "scale"},
    "boxplot":   {"duration": 600, "easing": "quartOut", "type": "scale"},
    "tree":      {"duration": 800, "easing": "quartOut", "type": "scale"},
    "sankey":    {"duration": 800, "easing": "quartOut", "type": "scale"},
    "graph":     {"duration": 1200, "easing": "quartOut", "type": "scale"},
    "calendar":  {"duration": 800, "easing": "quartOut", "type": "scale"},
    "wordcloud": {"duration": 800, "easing": "quartOut", "type": "scale"},
}

_SERIES_STAGGER_MS = 120


# ── Internal helpers ────────────────────────────────────────────────────

def _base_option(title="", subtitle=""):
    opt = {
        "backgroundColor": "transparent",
        "textStyle": {"fontFamily": "Noto Sans"},
        "title": {
            "text": title,
            "textStyle": {
                "fontFamily": "Noto Sans",
                "fontWeight": 600,
                "fontSize": 14,
                "color": TL_LIGHT["text"],
            },
            "subtextStyle": {
                "fontFamily": "Noto Sans",
                "fontSize": 11,
                "color": TL_LIGHT["text_muted"],
            },
            "left": "center",
            "top": 4,
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": TL_LIGHT["bg"],
            "borderColor": TL_LIGHT["zeroline"],
            "textStyle": {
                "fontFamily": "Noto Sans",
                "fontSize": 12,
                "color": TL_LIGHT["text"],
            },
            "borderRadius": 6,
            "extraCssText": "box-shadow: 0 2px 8px rgba(0,0,0,0.08);",
        },
        "legend": {
            "textStyle": {
                "fontFamily": "Noto Sans",
                "fontSize": 11,
                "color": TL_LIGHT["text_secondary"],
            },
            "bottom": 0,
            "icon": "roundRect",
            "itemWidth": 12,
            "itemHeight": 8,
        },
        "grid": {
            "containLabel": True,
            "left": 16,
            "right": 16,
            "top": 56,
            "bottom": 48,
        },
        "aria": {"enabled": True, "decal": {"show": True}},
        "animationType": "scale",
        "animationEasing": "quartOut",
        "animationDuration": 600,
    }
    if subtitle:
        opt["title"]["subtext"] = subtitle
    return opt


def _cat_axis(labels=None, name=""):
    ax = {
        "type": "category",
        "axisLabel": {
            "fontFamily": "Noto Sans Mono",
            "fontSize": 10,
            "color": TL_LIGHT["text_muted"],
        },
        "axisLine": {"lineStyle": {"color": TL_LIGHT["zeroline"]}},
        "axisTick": {"lineStyle": {"color": TL_LIGHT["zeroline"]}},
        "splitLine": {"show": False},
    }
    if labels is not None:
        ax["data"] = [str(l) for l in labels]
    if name:
        ax["name"] = name
        ax["nameTextStyle"] = {
            "fontFamily": "Noto Sans",
            "fontSize": 11,
            "color": TL_LIGHT["text_secondary"],
        }
        ax["nameLocation"] = "middle"
        ax["nameGap"] = 30
    return ax


def _val_axis(name="", format_str=None):
    ax = {
        "type": "value",
        "axisLabel": {
            "fontFamily": "Noto Sans Mono",
            "fontSize": 10,
            "color": TL_LIGHT["text_muted"],
        },
        "axisLine": {"lineStyle": {"color": TL_LIGHT["zeroline"]}},
        "axisTick": {"lineStyle": {"color": TL_LIGHT["zeroline"]}},
        "splitLine": {"lineStyle": {"color": TL_LIGHT["grid"], "type": "solid"}},
    }
    if name:
        ax["name"] = name
        ax["nameTextStyle"] = {
            "fontFamily": "Noto Sans",
            "fontSize": 11,
            "color": TL_LIGHT["text_secondary"],
        }
        ax["nameLocation"] = "middle"
        ax["nameGap"] = 46
    if format_str:
        ax["axisLabel"]["formatter"] = format_str
    return ax


def _to_series(raw_series, chart_type="bar", stagger=True):
    """Convert legacy series list to ECharts series list."""
    result = []
    for i, s in enumerate(raw_series):
        es = {
            "name": s.get("text", s.get("name", "")),
            "type": chart_type,
            "data": s.get("values", s.get("data", [])),
            "itemStyle": {"color": s.get("backgroundColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])},
        }
        if chart_type == "line":
            es["lineStyle"] = {"color": s.get("lineColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)]), "width": 2}
            es["symbol"] = "circle"
            es["symbolSize"] = 5
            es["itemStyle"]["color"] = s.get("lineColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])
        if stagger and len(raw_series) > 1:
            es["animationDelay"] = i * _SERIES_STAGGER_MS
        for k, v in s.items():
            if k not in ("text", "name", "values", "data", "backgroundColor", "lineColor", "type"):
                es[k] = v
        result.append(es)
    return result


def _convert_treemap_node(node):
    """Recursively convert legacy treemap nodes to ECharts format."""
    result = {"name": node.get("text", node.get("name", ""))}
    if "value" in node:
        result["value"] = node["value"]
    if "children" in node:
        result["children"] = [_convert_treemap_node(c) for c in node["children"]]
    return result


def _apply_anim(option, chart_type):
    cfg = _ANIM.get(chart_type, _ANIM["bar"])
    option["animationDuration"] = cfg["duration"]
    option["animationEasing"] = cfg["easing"]
    option["animationType"] = cfg.get("type", "scale")


# ── Utility functions ───────────────────────────────────────────────────

def add_source_annotation(option, source_system, date="April 2026"):
    """Add source attribution as title subtext."""
    source_text = f"Source: {source_system}, extracted {date}"
    title = option.setdefault("title", {})
    existing = title.get("subtext", "")
    title["subtext"] = f"{existing}  |  {source_text}" if existing else source_text
    title.setdefault("subtextStyle", {
        "fontFamily": "Noto Sans",
        "fontSize": 10,
        "color": TL_LIGHT["text_muted"],
    })
    return option


def add_crosshair(option):
    option["tooltip"] = {
        **option.get("tooltip", {}),
        "trigger": "axis",
        "axisPointer": {
            "type": "cross",
            "crossStyle": {"color": TL_LIGHT["zeroline"]},
            "label": {
                "fontFamily": "Noto Sans Mono",
                "fontSize": 10,
                "backgroundColor": TL_LIGHT["text"],
                "color": TL_LIGHT["bg"],
                "borderRadius": 4,
            },
        },
    }
    return option


def add_zoom_preview(option):
    option["dataZoom"] = [
        {
            "type": "slider",
            "show": True,
            "bottom": 8,
            "height": 20,
            "borderColor": TL_LIGHT["border"],
            "fillerColor": TL_CATEGORICAL[0] + "18",
            "handleStyle": {"color": TL_CATEGORICAL[0]},
            "textStyle": {"fontFamily": "Noto Sans Mono", "fontSize": 10, "color": TL_LIGHT["text_muted"]},
        },
        {"type": "inside"},
    ]
    option.setdefault("grid", {})["bottom"] = 72
    return option


def add_animation(option, chart_type="bar"):
    _apply_anim(option, chart_type)
    return option


def add_toolbox(option):
    option["toolbox"] = {
        "show": True,
        "right": 16,
        "top": 4,
        "feature": {
            "saveAsImage": {"title": "Save as PNG", "pixelRatio": 2},
            "dataView": {"title": "Data", "readOnly": True,
                         "textareaColor": TL_LIGHT["bg"],
                         "textColor": TL_LIGHT["text"]},
            "restore": {"title": "Reset"},
        },
        "iconStyle": {"borderColor": TL_LIGHT["text_muted"]},
        "emphasis": {"iconStyle": {"borderColor": TL_LIGHT["text"]}},
    }
    return option


def add_reference_line(option, axis, value, label, color=None):
    """Add a dashed reference markLine on the given axis ('x' or 'y')."""
    line_color = color or TL_LIGHT["text_muted"]
    ml = {
        "silent": True,
        "symbol": "none",
        "lineStyle": {"type": "dashed", "color": line_color, "width": 1},
        "label": {
            "formatter": label,
            "fontFamily": "Noto Sans",
            "fontSize": 10,
            "color": line_color,
            "position": "insideEndTop",
        },
    }
    if axis == "y":
        ml["yAxis"] = value
    else:
        ml["xAxis"] = value
    for s in option.get("series", []):
        s.setdefault("markLine", {"data": []})["data"].append(ml)
        break
    return option


# ── Standard chart builders ─────────────────────────────────────────────

def bar_config(categories, series, *, horizontal=False, stacked=False, title="", source="",
               x_title="", y_title=""):
    """Build a bar chart option.

    series: list of dicts with 'text' (legend label) and 'values' (list of numbers).
    """
    option = _base_option(title)
    cat_ax = _cat_axis(labels=categories, name=y_title if horizontal else x_title)
    val_ax = _val_axis(name=x_title if horizontal else y_title)

    if horizontal:
        option["xAxis"] = val_ax
        option["yAxis"] = cat_ax
        option["tooltip"]["trigger"] = "axis"
    else:
        option["xAxis"] = cat_ax
        option["yAxis"] = val_ax

    ec_series = _to_series(series, "bar")
    if stacked:
        for s in ec_series:
            s["stack"] = "total"
    option["series"] = ec_series

    _apply_anim(option, "bar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def line_config(categories, series, *, title="", source="", x_title="", y_title="",
                crosshair=True):
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=categories, name=x_title)
    option["yAxis"] = _val_axis(name=y_title)
    option["series"] = _to_series(series, "line")

    _apply_anim(option, "line")
    add_toolbox(option)
    if crosshair:
        add_crosshair(option)
    if source:
        add_source_annotation(option, source)
    return option


def histogram_config(bin_edges, bin_counts, *, title="", source="", x_title="", y_title="Count"):
    labels = [str(e) for e in bin_edges[:-1]] if len(bin_edges) > len(bin_counts) else [str(e) for e in bin_edges]
    return bar_config(labels, [{"text": "Count", "values": bin_counts}],
                      title=title, source=source, x_title=x_title, y_title=y_title)


def treemap_config(children, *, title="", source=""):
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["trigger"] = "item"
    option["series"] = [{
        "type": "treemap",
        "data": [_convert_treemap_node(c) for c in children],
        "breadcrumb": {"show": True, "itemStyle": {"color": TL_LIGHT["bg"]},
                       "textStyle": {"fontFamily": "Noto Sans", "fontSize": 11, "color": TL_LIGHT["text_secondary"]}},
        "label": {"fontFamily": "Noto Sans", "fontSize": 11, "color": TL_LIGHT["text"]},
        "levels": [
            {"itemStyle": {"borderColor": TL_LIGHT["border"], "borderWidth": 2, "gapWidth": 2}},
            {"colorSaturation": [0.35, 0.5],
             "itemStyle": {"borderColor": TL_LIGHT["border"], "borderWidth": 1, "gapWidth": 1}},
        ],
        "color": TL_CATEGORICAL,
    }]
    _apply_anim(option, "treemap")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def sunburst_config(data, *, title="", source=""):
    option = _base_option(title)
    del option["grid"]
    option["tooltip"]["trigger"] = "item"

    def _convert_sunburst(node):
        r = {"name": node.get("text", node.get("name", ""))}
        if "value" in node:
            r["value"] = node["value"]
        if "children" in node:
            r["children"] = [_convert_sunburst(c) for c in node["children"]]
        return r

    option["series"] = [{
        "type": "sunburst",
        "data": [_convert_sunburst(d) for d in data],
        "radius": ["15%", "90%"],
        "label": {"fontFamily": "Noto Sans", "fontSize": 10, "color": TL_LIGHT["text"]},
        "itemStyle": {"borderColor": TL_LIGHT["bg"], "borderWidth": 2},
        "color": TL_CATEGORICAL,
    }]
    _apply_anim(option, "sunburst")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def heatmap_config(matrix, x_labels, y_labels, *, title="", source="", min_val=None, max_val=None):
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=x_labels)
    option["yAxis"] = _cat_axis(labels=y_labels)
    option["tooltip"]["trigger"] = "item"

    data = []
    flat_vals = []
    for yi, row in enumerate(matrix):
        for xi, val in enumerate(row if isinstance(row, (list, tuple)) else [row]):
            if val is not None:
                data.append([xi, yi, val])
                flat_vals.append(val)

    lo = min_val if min_val is not None else (min(flat_vals) if flat_vals else 0)
    hi = max_val if max_val is not None else (max(flat_vals) if flat_vals else 1)

    option["visualMap"] = {
        "min": lo, "max": hi,
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": 4,
        "inRange": {"color": TL_SEQUENTIAL},
        "textStyle": {"fontFamily": "Noto Sans Mono", "fontSize": 10, "color": TL_LIGHT["text_muted"]},
    }
    option["series"] = [{
        "type": "heatmap",
        "data": data,
        "label": {"show": True, "fontFamily": "Noto Sans Mono", "fontSize": 9,
                  "color": TL_LIGHT["text"]},
        "emphasis": {"itemStyle": {"shadowBlur": 6, "shadowColor": "rgba(0,0,0,0.15)"}},
    }]
    option["grid"]["bottom"] = 64
    _apply_anim(option, "heatmap")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def boxplot_config(datasets, labels, *, title="", source=""):
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=labels)
    option["yAxis"] = _val_axis()
    option["tooltip"]["trigger"] = "item"

    series_data = []
    for i, d in enumerate(datasets):
        vals = d.get("values", d.get("data-box", []))
        if isinstance(vals, (list, tuple)) and len(vals) > 0:
            if isinstance(vals[0], (list, tuple)):
                series_data.append(vals[0])
            else:
                sorted_v = sorted(vals)
                n = len(sorted_v)
                if n >= 5:
                    series_data.append([
                        sorted_v[0],
                        sorted_v[n // 4],
                        sorted_v[n // 2],
                        sorted_v[(3 * n) // 4],
                        sorted_v[-1],
                    ])
                else:
                    series_data.append(sorted_v + [0] * (5 - n))

    option["series"] = [{
        "type": "boxplot",
        "data": series_data,
        "itemStyle": {"color": TL_CATEGORICAL[0], "borderColor": TL_CATEGORICAL[0]},
    }]
    _apply_anim(option, "boxplot")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def chord_config(matrix, labels, *, title="", source=""):
    option = _base_option(title)
    del option["grid"]
    option["tooltip"]["trigger"] = "item"

    nodes = [{"name": str(l)} for l in labels]
    for i, n in enumerate(nodes):
        n["itemStyle"] = {"color": TL_CATEGORICAL[i % len(TL_CATEGORICAL)]}

    links = []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val and val > 0 and i != j:
                links.append({"source": str(labels[i]), "target": str(labels[j]), "value": val})

    option["series"] = [{
        "type": "chord",
        "data": nodes,
        "links": links,
        "label": {"fontFamily": "Noto Sans", "fontSize": 10, "color": TL_LIGHT["text"]},
        "lineStyle": {"opacity": 0.4},
        "emphasis": {"lineStyle": {"opacity": 0.7}},
    }]
    _apply_anim(option, "chord")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def scatter_config(data, *, title="", source="", x_title="", y_title=""):
    option = _base_option(title)
    option["xAxis"] = _val_axis(name=x_title)
    option["yAxis"] = _val_axis(name=y_title)
    option["tooltip"]["trigger"] = "item"

    raw = data if isinstance(data, list) else [data]
    ec_series = []
    for i, s in enumerate(raw):
        vals = s.get("values", s.get("data", []))
        total_points = len(vals) if isinstance(vals, list) else 0
        es = {
            "name": s.get("text", s.get("name", "")),
            "type": "scatter",
            "data": vals,
            "itemStyle": {"color": s.get("backgroundColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])},
            "symbolSize": 6,
        }
        if total_points > 2000:
            es["large"] = True
            es["largeThreshold"] = 2000
            es["progressive"] = 400
            es["progressiveThreshold"] = 3000
        ec_series.append(es)
    option["series"] = ec_series
    _apply_anim(option, "scatter")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def mixed_config(series_list, *, title="", source="", categories=None, x_title="", y_title=""):
    option = _base_option(title)
    if categories:
        option["xAxis"] = _cat_axis(labels=categories, name=x_title)
    else:
        option["xAxis"] = _val_axis(name=x_title)
    option["yAxis"] = _val_axis(name=y_title)

    ec_series = []
    for i, s in enumerate(series_list):
        chart_type = s.get("type", "bar")
        es = {
            "name": s.get("text", s.get("name", "")),
            "type": chart_type,
            "data": s.get("values", s.get("data", [])),
            "itemStyle": {"color": s.get("backgroundColor", s.get("lineColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)]))},
        }
        if chart_type == "line":
            es["lineStyle"] = {"color": es["itemStyle"]["color"], "width": 2}
            es["symbol"] = "circle"
            es["symbolSize"] = 5
        if len(series_list) > 1:
            es["animationDelay"] = i * _SERIES_STAGGER_MS
        ec_series.append(es)
    option["series"] = ec_series
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


# ── Advanced showcase chart builders ────────────────────────────────────

def radar_config(axes, series, *, title="", source=""):
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["trigger"] = "item"

    option["radar"] = {
        "indicator": [{"name": a, "max": 100} for a in axes],
        "axisName": {"fontFamily": "Noto Sans", "fontSize": 10, "color": TL_LIGHT["text_secondary"]},
        "splitArea": {"areaStyle": {"color": "transparent"}},
        "splitLine": {"lineStyle": {"color": TL_LIGHT["grid"]}},
        "axisLine": {"lineStyle": {"color": TL_LIGHT["grid"]}},
    }

    ec_series = []
    for i, s in enumerate(series):
        color = s.get("lineColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])
        ec_series.append({
            "type": "radar",
            "name": s.get("text", s.get("name", "")),
            "data": [{"value": s["values"], "name": s.get("text", "")}],
            "lineStyle": {"color": color, "width": 2},
            "areaStyle": {"color": color, "opacity": 0.15},
            "itemStyle": {"color": color},
            "symbol": "circle",
            "symbolSize": 5,
            "animationDelay": i * _SERIES_STAGGER_MS,
        })
    option["series"] = ec_series
    _apply_anim(option, "radar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def bullet_config(items, *, title=""):
    """Build a gauge-based bullet chart.

    items: list of dicts with 'label', 'actual', 'target', 'ranges'.
    Rendered as stacked gauges with gradient arcs and target markers.
    """
    return gauge_multi_config([
        {
            "label": item.get("label", ""),
            "value": item.get("actual", 0),
            "max": max(item.get("ranges", [100])[-1:] or [100], default=100),
            "target": item.get("target"),
            "thresholds": _ranges_to_thresholds(item.get("ranges", [])),
        }
        for item in items
    ], title=title)


def _ranges_to_thresholds(ranges):
    if not ranges or len(ranges) < 2:
        return [[0.3, TL_STATUS["red"]], [0.7, TL_STATUS["amber"]], [1.0, TL_STATUS["green"]]]
    total = max(ranges[-1], 1)
    return [
        [ranges[0] / total, TL_STATUS["red"] + "40"],
        [ranges[1] / total if len(ranges) > 1 else 0.7, TL_STATUS["amber"] + "40"],
        [1.0, TL_STATUS["green"] + "40"],
    ]


def waterfall_config(categories, values, *, title="", source=""):
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=categories)
    option["yAxis"] = _val_axis(name="$USD")
    option["tooltip"]["trigger"] = "axis"

    base_vals = []
    bar_vals = []
    running = 0
    for i, v in enumerate(values):
        if i == len(values) - 1:
            base_vals.append(0)
            bar_vals.append(running + v if v >= 0 else running)
        else:
            if v >= 0:
                base_vals.append(running)
                bar_vals.append(v)
                running += v
            else:
                running += v
                base_vals.append(running)
                bar_vals.append(abs(v))

    option["series"] = [
        {
            "name": "Base",
            "type": "bar",
            "stack": "waterfall",
            "data": base_vals,
            "itemStyle": {"color": "transparent", "borderColor": "transparent"},
            "emphasis": {"itemStyle": {"color": "transparent"}},
        },
        {
            "name": "Value",
            "type": "bar",
            "stack": "waterfall",
            "data": [{"value": v, "itemStyle": {"color": TL_LIGHT["text"] if i == len(bar_vals) - 1
                      else (TL_STATUS["green"] if values[i] >= 0 else TL_STATUS["red"])}}
                     for i, v in enumerate(bar_vals)],
            "label": {"show": True, "position": "top", "fontFamily": "Noto Sans Mono",
                      "fontSize": 10, "color": TL_LIGHT["text"]},
        },
    ]
    _apply_anim(option, "bar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def pareto_config(categories, values, *, title="", source=""):
    """Dual-axis pareto: bar (left) + cumulative % line (right), color-coded."""
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=categories)

    bar_color = TL_CATEGORICAL[0]
    line_color = TL_CATEGORICAL[3]

    option["yAxis"] = [
        {**_val_axis(), "axisLine": {"lineStyle": {"color": bar_color}},
         "axisLabel": {**_val_axis()["axisLabel"], "color": bar_color}},
        {**_val_axis(), "axisLine": {"lineStyle": {"color": line_color}},
         "axisLabel": {**_val_axis()["axisLabel"], "color": line_color, "formatter": "{value}%"},
         "min": 0, "max": 100, "splitLine": {"show": False}},
    ]

    total = sum(values) if values else 1
    cumulative = []
    running = 0
    for v in values:
        running += v
        cumulative.append(round(running / total * 100, 1))

    option["series"] = [
        {"name": "Count", "type": "bar", "data": values,
         "itemStyle": {"color": bar_color}, "yAxisIndex": 0,
         "animationDelay": 0},
        {"name": "Cumulative %", "type": "line", "data": cumulative,
         "yAxisIndex": 1, "lineStyle": {"color": line_color, "width": 2},
         "itemStyle": {"color": line_color}, "symbol": "circle", "symbolSize": 5,
         "animationDelay": _SERIES_STAGGER_MS},
    ]
    option["grid"]["right"] = 56
    _apply_anim(option, "bar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def violin_config(datasets, labels, *, title="", source=""):
    """Violin approximation using boxplot (built-in). Custom violin renderItem
    available via @echarts-x/custom-violin extension for richer output."""
    return boxplot_config(datasets, labels, title=title, source=source)


def bubble_config(data, *, title="", source="", x_title="", y_title=""):
    option = _base_option(title)
    option["xAxis"] = _val_axis(name=x_title)
    option["yAxis"] = _val_axis(name=y_title)
    option["tooltip"]["trigger"] = "item"

    raw = data if isinstance(data, list) else [data]
    ec_series = []
    for i, s in enumerate(raw):
        vals = s.get("values", s.get("data", []))
        ec_series.append({
            "name": s.get("text", s.get("name", "")),
            "type": "scatter",
            "data": vals,
            "itemStyle": {"color": s.get("backgroundColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)]),
                          "opacity": 0.7},
            "symbolSize": "__BUBBLE__",
            "animationDelay": i * _SERIES_STAGGER_MS,
        })
    option["series"] = ec_series
    option["_bubble"] = True
    _apply_anim(option, "scatter")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def calendar_config(date_values, *, title="", source="", year=2026):
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)

    cal_data = []
    for entry in date_values:
        if isinstance(entry, (list, tuple)) and len(entry) >= 2:
            cal_data.append([str(entry[0]), entry[1]])
        elif isinstance(entry, dict):
            cal_data.append([entry.get("date", ""), entry.get("value", 0)])

    flat_vals = [d[1] for d in cal_data if isinstance(d[1], (int, float))]
    lo = min(flat_vals) if flat_vals else 0
    hi = max(flat_vals) if flat_vals else 1

    option["calendar"] = {
        "top": 60, "left": 40, "right": 16,
        "cellSize": ["auto", 16],
        "range": str(year),
        "itemStyle": {"borderWidth": 2, "borderColor": TL_LIGHT["bg"]},
        "dayLabel": {"nameMap": "en", "fontFamily": "Noto Sans Mono", "fontSize": 9,
                     "color": TL_LIGHT["text_muted"]},
        "monthLabel": {"fontFamily": "Noto Sans", "fontSize": 10, "color": TL_LIGHT["text_secondary"]},
        "yearLabel": {"show": False},
        "splitLine": {"lineStyle": {"color": TL_LIGHT["border"]}},
    }
    option["visualMap"] = {
        "min": lo, "max": hi, "calculable": True,
        "orient": "horizontal", "left": "center", "bottom": 4,
        "inRange": {"color": TL_SEQUENTIAL},
        "textStyle": {"fontFamily": "Noto Sans Mono", "fontSize": 10, "color": TL_LIGHT["text_muted"]},
    }
    option["series"] = [{
        "type": "heatmap",
        "coordinateSystem": "calendar",
        "data": cal_data,
    }]
    _apply_anim(option, "calendar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def funnel_config(stages, *, title="", source=""):
    option = _base_option(title)
    del option["grid"]
    option["tooltip"]["trigger"] = "item"

    option["series"] = [{
        "type": "funnel",
        "left": "10%",
        "top": 60,
        "bottom": 40,
        "width": "80%",
        "sort": "descending",
        "gap": 2,
        "label": {"show": True, "position": "inside", "fontFamily": "Noto Sans",
                  "fontSize": 11, "color": "#fff"},
        "labelLine": {"show": False},
        "itemStyle": {"borderColor": TL_LIGHT["bg"], "borderWidth": 1},
        "emphasis": {"label": {"fontSize": 13}},
        "data": [
            {"name": s["text"], "value": s["values"][0] if s.get("values") else 0,
             "itemStyle": {"color": TL_CATEGORICAL[i % len(TL_CATEGORICAL)]}}
            for i, s in enumerate(stages)
        ],
    }]
    _apply_anim(option, "funnel")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def rankflow_config(periods, series, *, title="", source=""):
    """Bump/rankflow chart implemented as a styled line chart with inverted rank y-axis."""
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=periods)
    option["yAxis"] = {
        **_val_axis(),
        "inverse": True,
        "min": 1,
        "max": len(series),
        "interval": 1,
        "axisLabel": {"fontFamily": "Noto Sans Mono", "fontSize": 10,
                      "color": TL_LIGHT["text_muted"], "formatter": "#{value}"},
    }

    ec_series = []
    for i, s in enumerate(series):
        color = TL_CATEGORICAL[i % len(TL_CATEGORICAL)]
        ec_series.append({
            "name": s.get("text", s.get("name", "")),
            "type": "line",
            "data": s.get("ranks", s.get("values", [])),
            "smooth": 0.3,
            "lineStyle": {"color": color, "width": 3},
            "itemStyle": {"color": color},
            "symbol": "circle",
            "symbolSize": 8,
            "animationDelay": i * _SERIES_STAGGER_MS,
        })
    option["series"] = ec_series
    _apply_anim(option, "line")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def range_config(categories, ranges, *, title="", source="", horizontal=True):
    """Range chart showing [low, high] bars per category."""
    option = _base_option(title)
    option["tooltip"]["trigger"] = "axis"

    low_vals = [r[0] if isinstance(r, (list, tuple)) and len(r) >= 2 else 0 for r in ranges]
    high_vals = [r[1] - r[0] if isinstance(r, (list, tuple)) and len(r) >= 2 else 0 for r in ranges]

    if horizontal:
        option["yAxis"] = _cat_axis(labels=categories)
        option["xAxis"] = _val_axis()
    else:
        option["xAxis"] = _cat_axis(labels=categories)
        option["yAxis"] = _val_axis()

    option["series"] = [
        {"name": "Low", "type": "bar", "stack": "range",
         "data": low_vals,
         "itemStyle": {"color": "transparent", "borderColor": "transparent"},
         "emphasis": {"itemStyle": {"color": "transparent"}}},
        {"name": "Range", "type": "bar", "stack": "range",
         "data": high_vals,
         "itemStyle": {"color": TL_CATEGORICAL[0], "opacity": 0.7},
         "label": {"show": True, "position": "inside", "fontFamily": "Noto Sans Mono",
                   "fontSize": 9, "color": "#fff"}},
    ]
    _apply_anim(option, "bar")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def wordcloud_config(words, *, title="", source=""):
    """words: list of [text, count] pairs."""
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["trigger"] = "item"

    option["series"] = [{
        "type": "wordCloud",
        "shape": "circle",
        "gridSize": 8,
        "sizeRange": [12, 48],
        "rotationRange": [-45, 45],
        "rotationStep": 45,
        "textStyle": {"fontFamily": "Noto Sans", "fontWeight": 500,
                      "color": "__WORDCLOUD_COLOR__"},
        "emphasis": {"textStyle": {"shadowBlur": 6, "shadowColor": "rgba(0,0,0,0.15)"}},
        "data": [{"name": w[0], "value": w[1]} for w in words],
    }]
    option["_wordcloud"] = True
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def venn_config(sets, *, title="", source=""):
    """Venn diagram rendered with ECharts graphic component overlay."""
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["show"] = False

    graphics = []
    cx, cy = 300, 220
    r = 120
    positions = [(-50, -20), (50, -20), (0, 40)]

    for i, s in enumerate(sets):
        px, py = positions[i % 3]
        color = s.get("backgroundColor", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])
        text = s.get("text", s.get("name", ""))
        val = s.get("values", s.get("data", [0]))[0] if isinstance(s.get("values", s.get("data", [])), list) else ""
        graphics.append({
            "type": "circle",
            "shape": {"cx": cx + px, "cy": cy + py, "r": r},
            "style": {"fill": color, "opacity": 0.25, "stroke": color, "lineWidth": 2},
        })
        graphics.append({
            "type": "text",
            "style": {"text": f"{text}\n{val}", "x": cx + px, "y": cy + py,
                      "fill": TL_LIGHT["text"], "fontSize": 12, "fontFamily": "Noto Sans",
                      "fontWeight": 500, "textAlign": "center", "textVerticalAlign": "middle"},
        })
    option["graphic"] = {"elements": graphics}
    option["series"] = []
    if source:
        add_source_annotation(option, source)
    return option


# ── New builders ────────────────────────────────────────────────────────

def gauge_config(value, *, title="", min_val=0, max_val=100,
                 thresholds=None, unit="%", target=None, delta=None, source=""):
    """Rich gauge with gradient arc, animated value, and threshold bands."""
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["show"] = False

    if thresholds is None:
        thresholds = [[0.3, TL_STATUS["red"]], [0.7, TL_STATUS["amber"]], [1.0, TL_STATUS["green"]]]

    detail_text = f"{{value}}{unit}"
    if delta:
        detail_text = f"{{value}}{unit}\n{delta}"

    option["series"] = [{
        "type": "gauge",
        "center": ["50%", "60%"],
        "radius": "80%",
        "min": min_val,
        "max": max_val,
        "startAngle": 225,
        "endAngle": -45,
        "axisLine": {"lineStyle": {"width": 14, "color": thresholds}},
        "progress": {"show": True, "width": 14,
                     "itemStyle": {"color": TL_CATEGORICAL[0]}},
        "pointer": {"show": bool(target), "length": "60%", "width": 4,
                    "itemStyle": {"color": TL_LIGHT["text"]}},
        "axisTick": {"show": False},
        "splitLine": {"show": False},
        "axisLabel": {"show": False},
        "detail": {
            "valueAnimation": True,
            "formatter": detail_text,
            "fontFamily": "Noto Sans Mono",
            "fontWeight": 600,
            "fontSize": 28,
            "color": TL_LIGHT["text"],
            "offsetCenter": [0, "30%"],
        },
        "title": {
            "fontFamily": "Noto Sans",
            "fontWeight": 500,
            "fontSize": 12,
            "color": TL_LIGHT["text_secondary"],
            "offsetCenter": [0, "55%"],
        },
        "data": [{"value": value, "name": title}],
        "animationDuration": 1200,
        "animationEasing": "elasticOut",
    }]
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def gauge_multi_config(metrics, *, title=""):
    """Multi-ring gauge panel with concentric rings for parallel KPIs.

    metrics: list of dicts with 'label', 'value', 'max', optional 'color',
             optional 'thresholds', optional 'target', optional 'unit'.
    """
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["show"] = False

    n = len(metrics)
    ec_series = []
    for i, m in enumerate(metrics):
        radius_pct = 85 - i * (60 // max(n, 1))
        arc_width = max(6, 14 - i * 2)
        color = m.get("color", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])
        thresholds = m.get("thresholds",
                           [[0.3, TL_STATUS["red"] + "30"], [0.7, TL_STATUS["amber"] + "30"],
                            [1.0, TL_STATUS["green"] + "30"]])
        unit = m.get("unit", "%")

        ec_series.append({
            "type": "gauge",
            "center": ["50%", "55%"],
            "radius": f"{radius_pct}%",
            "min": 0,
            "max": m.get("max", 100),
            "startAngle": 225,
            "endAngle": -45,
            "axisLine": {"lineStyle": {"width": arc_width, "color": thresholds}},
            "progress": {"show": True, "width": arc_width,
                         "itemStyle": {"color": color}},
            "pointer": {"show": False},
            "axisTick": {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "detail": {
                "valueAnimation": True,
                "formatter": f"{{value}}{unit}",
                "fontFamily": "Noto Sans Mono",
                "fontWeight": 600,
                "fontSize": 24 if i == 0 else 11,
                "color": TL_LIGHT["text"] if i == 0 else TL_LIGHT["text_secondary"],
                "offsetCenter": [0, f"{-20 + i * 28}%"] if i == 0 else [0, f"{-20 + i * 28}%"],
                "show": i == 0,
            },
            "title": {
                "fontFamily": "Noto Sans",
                "fontSize": 10,
                "color": TL_LIGHT["text_muted"],
                "offsetCenter": [f"{radius_pct - 4}%", "90%"],
                "show": True,
            },
            "data": [{"value": m["value"], "name": m.get("label", "")}],
            "animationDuration": 1200,
            "animationDelay": i * 200,
            "animationEasing": "elasticOut",
        })
    option["series"] = ec_series
    add_toolbox(option)
    return option


def dual_axis_config(categories, series_left, series_right, *,
                     title="", source="",
                     y_left_title="", y_right_title="",
                     left_type="bar", right_type="line"):
    """Dual y-axis chart with color-coded axes and yAxisIndex binding."""
    option = _base_option(title)
    option["xAxis"] = _cat_axis(labels=categories)

    l_color = TL_CATEGORICAL[0]
    r_color = TL_CATEGORICAL[3]

    option["yAxis"] = [
        {**_val_axis(name=y_left_title),
         "axisLine": {"show": True, "lineStyle": {"color": l_color}},
         "axisLabel": {**_val_axis()["axisLabel"], "color": l_color}},
        {**_val_axis(name=y_right_title),
         "axisLine": {"show": True, "lineStyle": {"color": r_color}},
         "axisLabel": {**_val_axis()["axisLabel"], "color": r_color},
         "splitLine": {"show": False}},
    ]

    ec_left = _to_series(series_left, left_type, stagger=False)
    for s in ec_left:
        s["yAxisIndex"] = 0
        s["itemStyle"]["color"] = l_color
        if left_type == "line":
            s["lineStyle"] = {"color": l_color, "width": 2}

    ec_right = _to_series(series_right, right_type, stagger=False)
    for s in ec_right:
        s["yAxisIndex"] = 1
        s["itemStyle"]["color"] = r_color
        if right_type == "line":
            s["lineStyle"] = {"color": r_color, "width": 2}
        s["animationDelay"] = _SERIES_STAGGER_MS

    option["series"] = ec_left + ec_right
    option["grid"]["right"] = 56
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def sankey_config(nodes, links, *, title="", source=""):
    """Sankey flow diagram."""
    option = _base_option(title)
    del option["grid"]
    option["tooltip"]["trigger"] = "item"

    for i, n in enumerate(nodes):
        n.setdefault("itemStyle", {}).setdefault("color", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])

    option["series"] = [{
        "type": "sankey",
        "data": nodes,
        "links": links,
        "emphasis": {"focus": "adjacency"},
        "lineStyle": {"color": "gradient", "curveness": 0.5, "opacity": 0.3},
        "label": {"fontFamily": "Noto Sans", "fontSize": 10, "color": TL_LIGHT["text"]},
        "nodeWidth": 20,
        "nodeGap": 12,
        "layoutIterations": 32,
    }]
    _apply_anim(option, "sankey")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def graph_config(nodes, edges, *, title="", source="", use_gl=False):
    """Force-directed network graph."""
    option = _base_option(title)
    del option["grid"]
    option.pop("xAxis", None)
    option.pop("yAxis", None)
    option["tooltip"]["trigger"] = "item"

    for i, n in enumerate(nodes):
        n.setdefault("itemStyle", {}).setdefault("color", TL_CATEGORICAL[i % len(TL_CATEGORICAL)])

    series_type = "graphGL" if use_gl and len(nodes) > 100 else "graph"
    series_def = {
        "type": series_type,
        "data": nodes,
        "links" if series_type == "graph" else "edges": edges,
        "label": {"show": True, "fontFamily": "Noto Sans", "fontSize": 9,
                  "color": TL_LIGHT["text"], "position": "right"},
        "lineStyle": {"color": "source", "curveness": 0, "opacity": 0.3},
        "emphasis": {"focus": "adjacency", "lineStyle": {"opacity": 0.7}},
        "roam": True,
        "draggable": True,
    }

    if series_type == "graph":
        series_def["layout"] = "force"
        series_def["force"] = {"repulsion": 200, "gravity": 0.05, "edgeLength": [40, 200],
                               "layoutAnimation": True}
    else:
        series_def["forceAtlas2"] = {"steps": 5, "jitterTolerance": 10,
                                     "gravity": 0.1, "scalingRatio": 2}

    option["series"] = [series_def]
    option["_use_gl"] = use_gl and len(nodes) > 100
    _apply_anim(option, "graph")
    add_toolbox(option)
    if source:
        add_source_annotation(option, source)
    return option


def beeswarm_config(data, *, title="", source="", x_title="", y_title=""):
    """ECharts v6 scatter with jitter for beeswarm visualization."""
    option = scatter_config(data, title=title, source=source, x_title=x_title, y_title=y_title)
    option["_beeswarm"] = True
    return option


def write_echarts_json(option, path):
    """Write an ECharts option dict as a JSON file for inline rendering.

    Strips internal flags into a _meta object so the client-side
    init script knows which post-processing to apply.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    meta = {
        "bubble": option.pop("_bubble", False),
        "wordcloud": option.pop("_wordcloud", False),
        "beeswarm": option.pop("_beeswarm", False),
        "use_gl": option.pop("_use_gl", False),
    }
    with open(path, "w") as f:
        json.dump({"_meta": meta, "option": option},
                  f, ensure_ascii=False, separators=(",", ":"))
