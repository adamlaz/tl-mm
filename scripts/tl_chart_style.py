"""Translation Layer chart style system.

Single source of truth for Plotly chart styling across all engagement scripts.
Implements the TL deliverable brand: Noto fonts, TL categorical/sequential/diverging
palettes, status colors, and dark-mode CSS injection for iframe-embedded charts.

Usage::

    import tl_chart_style
    tl_chart_style.register_templates()
    fig = px.bar(...)
    tl_chart_style.write_themed_html(fig, "analysis/charts/my_chart.json")
"""

import os

import plotly.io as pio

# ── Categorical palette (8 colors, max perceptual distance) ──────────────

TL_CATEGORICAL = [
    "#4A5FC4",  # Indigo
    "#2A9D8F",  # Teal
    "#C4973A",  # Amber (echoes TL brass)
    "#C4574A",  # Rose
    "#6B82A0",  # Slate Blue
    "#6FAA5C",  # Olive
    "#9A6B9A",  # Mauve
    "#B07A4A",  # Sienna
]

# Dark-mode lifted variants (same hues, higher lightness for dark bg)
TL_CATEGORICAL_DARK = [
    "#6B7FE0",
    "#3AC4B4",
    "#D4A74A",
    "#D46A5A",
    "#8A9EC0",
    "#8ACC7A",
    "#B48AB4",
    "#C89060",
]

# ── Sequential palette (warm, 6 stops) ──────────────────────────────────

TL_SEQUENTIAL = [
    [0.0, "#F5F0E6"],
    [0.2, "#E0D0AA"],
    [0.4, "#C4A870"],
    [0.6, "#A08040"],
    [0.8, "#7A5E28"],
    [1.0, "#5A3E18"],
]

TL_SEQUENTIAL_DARK = [
    [0.0, "#2A2420"],
    [0.2, "#4A3E28"],
    [0.4, "#7A6030"],
    [0.6, "#A08040"],
    [0.8, "#C4A060"],
    [1.0, "#E0C48A"],
]

# ── Diverging palette (red-neutral-green) ────────────────────────────────

TL_DIVERGING = [
    [0.0, "#B84030"],
    [0.25, "#D89080"],
    [0.5, "#F0EBE1"],
    [0.75, "#80C4A0"],
    [1.0, "#2A8A5A"],
]

TL_DIVERGING_DARK = [
    [0.0, "#D46A5A"],
    [0.25, "#A08070"],
    [0.5, "#3A3430"],
    [0.75, "#70A890"],
    [1.0, "#3AC4A0"],
]

# ── Status colors (fixed, never client-derived) ─────────────────────────

TL_STATUS = {
    "green": "#3AAA5C",
    "amber": "#C4973A",
    "red": "#CC4A3A",
    "green_bg": "#E8F5EC",
    "amber_bg": "#F5F0E6",
    "red_bg": "#F5E8E6",
}

# ── Hex anchors for light / dark surfaces ────────────────────────────────

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

# ── Plotly templates ─────────────────────────────────────────────────────

TL_TEMPLATE_LIGHT = {
    "layout": {
        "font": {
            "family": "Noto Sans, system-ui, sans-serif",
            "color": TL_LIGHT["text"],
            "size": 12,
        },
        "title": {
            "font": {
                "family": "Noto Sans, system-ui, sans-serif",
                "size": 16,
                "weight": 600,
            },
            "x": 0,
            "xanchor": "left",
        },
        "paper_bgcolor": TL_LIGHT["bg"],
        "plot_bgcolor": TL_LIGHT["bg"],
        "colorway": TL_CATEGORICAL,
        "colorscale": {
            "sequential": TL_SEQUENTIAL,
            "diverging": TL_DIVERGING,
        },
        "xaxis": {
            "gridcolor": TL_LIGHT["grid"],
            "zerolinecolor": TL_LIGHT["zeroline"],
            "linecolor": TL_LIGHT["zeroline"],
            "tickfont": {
                "family": "Noto Sans Mono, ui-monospace, monospace",
                "size": 10,
            },
            "title": {"font": {"size": 12}, "standoff": 12},
        },
        "yaxis": {
            "gridcolor": TL_LIGHT["grid"],
            "zerolinecolor": TL_LIGHT["zeroline"],
            "linecolor": TL_LIGHT["zeroline"],
            "tickfont": {
                "family": "Noto Sans Mono, ui-monospace, monospace",
                "size": 10,
            },
            "title": {"font": {"size": 12}, "standoff": 12},
        },
        "legend": {
            "font": {"size": 11},
            "bgcolor": "rgba(255,255,255,0)",
            "borderwidth": 0,
        },
        "hoverlabel": {
            "bgcolor": TL_LIGHT["bg"],
            "bordercolor": TL_LIGHT["zeroline"],
            "font": {
                "family": "Noto Sans, system-ui, sans-serif",
                "size": 12,
                "color": TL_LIGHT["text"],
            },
        },
        "margin": {"l": 60, "r": 20, "t": 60, "b": 50},
    }
}

TL_TEMPLATE_DARK = {
    "layout": {
        "font": {
            "family": "Noto Sans, system-ui, sans-serif",
            "color": TL_DARK["text"],
            "size": 12,
        },
        "title": {
            "font": {
                "family": "Noto Sans, system-ui, sans-serif",
                "size": 16,
                "weight": 600,
            },
            "x": 0,
            "xanchor": "left",
        },
        "paper_bgcolor": TL_DARK["bg"],
        "plot_bgcolor": TL_DARK["bg"],
        "colorway": TL_CATEGORICAL_DARK,
        "colorscale": {
            "sequential": TL_SEQUENTIAL_DARK,
            "diverging": TL_DIVERGING_DARK,
        },
        "xaxis": {
            "gridcolor": TL_DARK["grid"],
            "zerolinecolor": TL_DARK["zeroline"],
            "linecolor": TL_DARK["zeroline"],
            "tickfont": {
                "family": "Noto Sans Mono, ui-monospace, monospace",
                "size": 10,
                "color": TL_DARK["text_muted"],
            },
            "title": {
                "font": {"size": 12, "color": TL_DARK["text_secondary"]},
                "standoff": 12,
            },
        },
        "yaxis": {
            "gridcolor": TL_DARK["grid"],
            "zerolinecolor": TL_DARK["zeroline"],
            "linecolor": TL_DARK["zeroline"],
            "tickfont": {
                "family": "Noto Sans Mono, ui-monospace, monospace",
                "size": 10,
                "color": TL_DARK["text_muted"],
            },
            "title": {
                "font": {"size": 12, "color": TL_DARK["text_secondary"]},
                "standoff": 12,
            },
        },
        "legend": {
            "font": {"size": 11, "color": TL_DARK["text_secondary"]},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
        },
        "hoverlabel": {
            "bgcolor": "#2A2420",
            "bordercolor": TL_DARK["zeroline"],
            "font": {
                "family": "Noto Sans, system-ui, sans-serif",
                "size": 12,
                "color": TL_DARK["text"],
            },
        },
        "margin": {"l": 60, "r": 20, "t": 60, "b": 50},
    }
}

# Charts always render in light mode. Plotly bakes colors into inline SVG
# attributes (fill, stroke) on data traces -- CSS overrides can change
# backgrounds and text but cannot reach bar/line/marker colors. Attempting
# a CSS-only dark mode creates dark backgrounds with invisible data.
# The minisite's ChartEmbed component forces a white iframe background so
# the light chart always has a clean ground in both page themes.


def register_templates():
    """Register TL light/dark templates with Plotly and set light as default."""
    pio.templates["tl_light"] = TL_TEMPLATE_LIGHT
    pio.templates["tl_dark"] = TL_TEMPLATE_DARK
    pio.templates.default = "tl_light"


def apply_tl_style(fig):
    """Apply TL light template to an existing figure."""
    fig.update_layout(template=TL_TEMPLATE_LIGHT)
    return fig


def add_source_annotation(fig, source_system, date="April 2026"):
    """Add a standard source attribution annotation below the chart."""
    fig.add_annotation(
        text=f"Source: {source_system}, extracted {date}",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        showarrow=False,
        font=dict(
            family="Noto Sans, system-ui, sans-serif",
            size=10,
            color=TL_LIGHT["text_muted"],
        ),
        xanchor="left",
    )
    return fig


def write_themed_html(fig, path, *, include_plotlyjs="cdn"):
    """Write a Plotly figure to HTML with TL styling, responsive config, and CDN Plotly.

    The chart fills 100% of its container (the minisite iframe) and the modebar
    is always visible so users can zoom, pan, and download.
    """
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)

    fig.update_layout(
        autosize=True,
        height=None,
        margin=dict(
            l=fig.layout.margin.l or 60,
            r=fig.layout.margin.r or 20,
            t=fig.layout.margin.t or 60,
            b=max(fig.layout.margin.b or 50, 60),
        ),
    )

    html = fig.to_html(
        include_plotlyjs=include_plotlyjs,
        full_html=True,
        config={
            "responsive": True,
            "displayModeBar": True,
            "scrollZoom": True,
            "modeBarButtonsToAdd": ["pan2d", "zoomIn2d", "zoomOut2d", "resetScale2d"],
        },
    )

    fill_css = (
        '<style>'
        'html, body { margin: 0; padding: 0 12px; width: 100%; height: 100%; overflow: hidden; box-sizing: border-box; }'
        '.plotly-graph-div { width: 100% !important; height: 100% !important; }'
        '</style>'
    )
    html = html.replace("</head>", fill_css + "</head>", 1)

    with open(path, "w") as f:
        f.write(html)
