# Translation Layer — Data Visualization Style Guide

How data looks in all Translation Layer deliverables. Chart palettes, typography, annotation conventions, chart type selection, accessibility, and the Apache ECharts v6 builder system.

Data visualization is governed entirely by TL's own standard — never by client brand colors. Client accent palettes are often not optimized for data legibility: poor contrast ratios, insufficient hue separation between series, no color-blind-safe considerations. TL brings its own instruments here.

This file governs **how data looks**. For how deliverables look overall, see [`client-deliverable-style.md`](client-deliverable-style.md). For how we write, see [`writing-style.md`](writing-style.md).

---

## Chart Color System

TL's own OKLCH-derived palettes, consistent across all engagements. These are not derived from any client palette. They are engineered for maximum legibility, hue separation, and color-blind safety.

### Categorical Palette

Eight distinct colors for discrete data series. Designed for maximum perceptual distance between adjacent colors. Tested against deuteranopia, protanopia, and tritanopia simulations.

| Index | Name | OKLCH | Hex (approx) | Usage |
|---|---|---|---|---|
| 1 | Indigo | `oklch(52% 0.14 265)` | `#4A5FC4` | Primary series, default first color |
| 2 | Teal | `oklch(62% 0.12 195)` | `#2A9D8F` | Second series |
| 3 | Amber | `oklch(72% 0.14 75)` | `#C4973A` | Third series (anchored in TL brass) |
| 4 | Rose | `oklch(58% 0.16 15)` | `#C4574A` | Fourth series |
| 5 | Slate Blue | `oklch(60% 0.08 250)` | `#6B82A0` | Fifth series |
| 6 | Olive | `oklch(65% 0.12 130)` | `#6FAA5C` | Sixth series |
| 7 | Mauve | `oklch(55% 0.10 320)` | `#9A6B9A` | Seventh series |
| 8 | Sienna | `oklch(58% 0.10 50)` | `#B07A4A` | Eighth series |

**Rules:**
- When a chart has fewer than 8 series, use colors in order starting from index 1
- Never reorder colors for aesthetic preference — consistency across charts matters more than any individual chart looking "balanced"
- If more than 8 series are needed, group smaller categories into "Other" rather than extending the palette
- The amber (index 3) intentionally echoes TL's brass — a subtle signature without dominating

### Sequential Palette

Single-hue ramp for magnitude, density, and continuous data. Anchored in TL's warm spectrum.

| Stop | OKLCH | Usage |
|---|---|---|
| 1 (low) | `oklch(95% 0.02 75)` | Minimum value / lowest density |
| 2 | `oklch(85% 0.06 75)` | |
| 3 | `oklch(72% 0.10 75)` | |
| 4 | `oklch(60% 0.13 75)` | |
| 5 | `oklch(48% 0.14 75)` | |
| 6 (high) | `oklch(35% 0.12 75)` | Maximum value / highest density |

Replaces Plotly's default purple-yellow sequential scale (`Viridis`). The warm hue connects to TL's brand without overwhelming the data.

### Diverging Palette

For above/below threshold, positive/negative, or before/after comparisons.

| Position | OKLCH | Represents |
|---|---|---|
| Negative extreme | `oklch(50% 0.18 25)` | Strong negative / below threshold |
| Negative moderate | `oklch(70% 0.10 25)` | Moderate negative |
| Neutral | `oklch(90% 0.01 80)` | Baseline / zero / threshold |
| Positive moderate | `oklch(70% 0.10 170)` | Moderate positive |
| Positive extreme | `oklch(50% 0.16 170)` | Strong positive / above threshold |

### Status Encoding

Reserved exclusively for pass/warn/fail, healthy/degraded/critical semantics. Not for general categorical use. These match the deliverable status tokens from [`client-deliverable-style.md`](client-deliverable-style.md).

| Status | OKLCH | Hex (approx) | Usage |
|---|---|---|---|
| Green (healthy) | `oklch(65% 0.17 145)` | `#3AAA5C` | Pass, healthy, on-track, complete |
| Amber (warning) | `oklch(75% 0.15 75)` | `#C4973A` | Warning, degraded, at-risk, partial |
| Red (critical) | `oklch(60% 0.20 25)` | `#CC4A3A` | Fail, critical, blocked, overdue |

**Rules:**
- Status colors are always paired with text labels — never the sole differentiator
- In bar charts, status-coded bars include text annotation of the status
- In tables, status colors appear as a cell background tint or a left-border indicator, always with text

### Chart Backgrounds

Charts must feel native to the page, not pasted from a different tool.

| Context | Background | Grid Lines |
|---|---|---|
| Light mode | `--surface` (white) | `--border-subtle` |
| Dark mode | `--surface` (dark neutral) | `--border-subtle` |
| Standalone HTML exports | `#FFFFFF` / `#1E1A1A` | `#E8E4DE` / `#2E2820` |

No `#E5ECF6` Plotly default. No colored plot backgrounds. The chart background matches the page surface.

---

## Typography in Charts

Noto family throughout, matching the deliverable type stack. No system fonts, no Syne, no JetBrains Mono.

| Element | Face | Weight | Size | Color Token |
|---|---|---|---|---|
| Chart title | Noto Sans | 600 | 14–16px | `--text` |
| Subtitle / description | Noto Sans | 400 | 12px | `--text-secondary` |
| Axis title | Noto Sans | 400 | 11–12px | `--text-secondary` |
| Tick labels | Noto Sans Mono | 400 | 10–11px | `--text-muted` |
| Data labels (on chart) | Noto Sans Mono | 400 | 10–11px | `--text` |
| Annotations / callouts | Noto Sans | 400 | 11px | `--text` |
| Legend | Noto Sans | 400 | 11px | `--text-secondary` |
| Hover tooltip title | Noto Sans | 600 | 12px | `--text` |
| Hover tooltip values | Noto Sans Mono | 400 | 11px | `--text` |

**Rules:**
- Tick labels and data values are always monospace (Noto Sans Mono) for tabular alignment
- Titles are sentence case, never all-caps
- Axis titles always present — no assumed context
- Legend text matches axis title styling

---

## Chart Type Selection Guide

When to use what. The right chart type eliminates the need for explanation.

### Bar Charts

**Horizontal bars** for comparison across categories. The category labels read naturally left-to-right without rotation. Preferred when category names are long (team names, tool names, project names).

**Vertical bars** for time series with discrete intervals (sprints, months, quarters). The x-axis reads as a timeline.

**Stacked bars** for part-to-whole composition. Use when the total AND the components both matter. Limit to 4–5 segments — more becomes illegible.

### Line Charts

Trends over continuous time. Connect data points only when interpolation between them is meaningful. If the data is discrete events with no meaningful interpolation (e.g., incident counts per month), use a bar chart.

Multiple lines on one chart: limit to 4–5 series. Beyond that, use small multiples or break into separate charts.

### Area Charts

Composition over time, stacked. Use when the total area matters as much as the individual series. Same 4–5 segment limit as stacked bars.

### Scatter Plots

Correlation between two continuous variables. Add a trend line when the correlation is the point of the chart. Label outliers directly on the chart.

### Heatmaps

Matrix comparison or density display. Ideal for time-of-day/day-of-week patterns, team-vs-metric matrices, or large comparison grids. Use the sequential palette. Always include a color legend with labeled stops.

### Network Graphs

Relationships and connection patterns: reviewer networks, dependency graphs, team interaction maps. Node size encodes importance (degree, centrality). Edge weight encodes frequency. Color-code by group (team, workspace, role).

### Treemaps

Hierarchical composition. Use when showing how a whole breaks into nested parts (repository structure, cost allocation, team distribution). Label tiles with both the name and the value.

### Avoid

| Chart Type | Why | Use Instead |
|---|---|---|
| Pie charts | Human perception of angles is poor. Comparing slices is harder than comparing bar lengths. | Horizontal bar chart |
| 3D charts | Depth distorts proportions. Perspective makes comparison impossible. | 2D equivalent |
| Donut charts | Same problems as pie, with even less area to encode data. | Horizontal bar chart |

### Use With Conditions

| Chart Type | When to Use | Requirements |
|---|---|---|
| Gauge charts | USE when a single KPI against a threshold range benefits from the visual arc showing position-within-range faster than a number alone. The gauge must be information-dense, not decorative. If a MetricCard communicates the same insight at the same speed, use the MetricCard. | Gradient arc with status color stops (green/amber/red). Animated value counter (`valueAnimation: true`). Rich center text: value (Noto Sans Mono 600, 28px), label (Noto Sans 500, 12px), optional delta in status green/red. No decorative ticks or speedometer chrome — the arc IS the information. Minimum arc thickness 10px. |
| Dual-axis charts | USE when two metrics share a causal or temporal relationship and showing them together reveals the relationship more clearly than two separate charts. The reader must never guess which axis belongs to which series. | Left and right y-axes visually distinct — axis line color, label color, and name color all match their series color (use `yAxisIndex` binding on every series). Explicit axis names with units ("Count", "$USD", "Percentage"). Tooltip shows both values together with labels. Grid right margin expanded to prevent right axis clipping. |

---

## Annotation and Labeling Conventions

Every chart must communicate its message without requiring the reader to puzzle over it.

### Required Elements

- **Descriptive title:** Not just the metric name. "Epic Completion Rate by Quarter" not "Completion Rate." "Pipeline Success Rate — Last 12 Months" not "Pipeline."
- **Axis labels:** Always present. Include units where applicable ("Count," "Hours," "Percentage," "$USD").
- **Source attribution:** Below the chart when data is external or from a specific system. "Source: Jira, extracted April 4, 2026."

### Conditional Elements

- **Data labels on bars:** Include when bar count is manageable (<15 bars). Omit when labels would overlap or clutter.
- **Trend lines:** Include with labeled slope or rate when the trend IS the insight. "−12% per quarter" as a text annotation on the line.
- **Reference lines:** Dashed, labeled, for benchmarks, thresholds, or industry standards. "DORA Elite: <1 hour" as a horizontal reference on a deployment frequency chart.
- **Annotations / callouts:** For notable events or outliers. "Reorg announced" as a vertical annotation on a time-series chart.

### Formatting Rules

- Rotated tick labels: −45 degrees maximum. Horizontal preferred. If labels must rotate beyond −45, the chart orientation is wrong — switch to horizontal bars.
- Margins: Generous. No clipped labels. Increase left margin for long category names, bottom margin for rotated ticks.
- Legend position: Outside the plot area, right side or top. Never overlapping data.
- Number formatting: Use locale-appropriate thousands separators. Abbreviate large numbers (1.2K, 3.4M) on axes but show full values in tooltips.

---

## Apache ECharts v6 Builder System

A reusable ECharts v6 theme and builder system that standardizes TL's chart style. Applied via `tl_echarts_style.py` builder functions which output JSON configs consumed inline by the minisite. The Astro minisite renders charts via `data-echarts` divs with embedded JSON and a client-side `echarts-init.ts` runtime that handles theme registration, scroll-triggered rendering, dark mode, and `prefers-reduced-motion` support.

### Usage

```python
import tl_echarts_style as zcs

config = zcs.bar_config(
    ["Q1", "Q2", "Q3"],
    [{"text": "Revenue", "values": [10, 20, 30]}],
    title="Revenue by Quarter",
    source="Jira"
)
zcs.write_echarts_json(config, "analysis/charts/revenue.json")
```

### Palette Constants

```python
TL_CATEGORICAL = [
    "#4A5FC4",  # Indigo
    "#2A9D8F",  # Teal
    "#C4973A",  # Amber (TL brass signature)
    "#C4574A",  # Rose
    "#6B82A0",  # Slate Blue
    "#6FAA5C",  # Olive
    "#9A6B9A",  # Mauve
    "#B07A4A",  # Sienna
]
TL_SEQUENTIAL = ["#F5F0E6", "#E0D0AA", "#C4A870", "#A08040", "#7A5E28", "#5A3E18"]
TL_DIVERGING = ["#B84030", "#D08060", "#F0E8DC", "#60C0A0", "#309878"]
TL_STATUS = {
    "green": "#3AAA5C",
    "amber": "#C4973A",
    "red":   "#CC4A3A",
    "green_bg": "#E8F5EC",
    "amber_bg": "#F5F0E6",
    "red_bg":   "#F5E8E6",
}
```

### Dark Mode

Dark mode is handled by the minisite's `echarts-init.ts` runtime. A `MutationObserver` watches the `data-theme` attribute on `<html>`. When it changes, all chart instances are disposed and reinitialized with the `tl-dark` registered theme. Dark mode uses elevated-lightness versions of all palette colors (`TL_CATEGORICAL_DARK`) and inverted surface tokens (`TL_DARK`).

### ECharts v6 Capabilities

Built into every chart via `tl_echarts_style.py`:

- **Toolbox**: Save-as-PNG, data view, and reset zoom on every chart
- **dataZoom**: Slider + scroll-to-zoom on time-series charts via `add_zoom_preview()`
- **Broken axes**: ECharts v6 torn-paper effect for magnitude gaps via `add_broken_axis()`
- **DORA reference lines**: Dashed `markLine` overlays via `add_reference_line()`
- **ARIA + decal patterns**: `aria: { enabled: true, decal: { show: true } }` on every chart
- **Canvas renderer**: GPU-composited with `useDirtyRect` for minimal redraws
- **Progressive rendering**: `large: true` mode for scatter/beeswarm with 2000+ points
- **Intersection Observer**: Charts render on scroll-into-view with type-specific entrance animations
- **`prefers-reduced-motion`**: All animations disabled; charts render fully formed instantly

### Chart Types Available

24 builder functions covering: bar, line, histogram, treemap, sunburst, heatmap, boxplot, chord (v6 native), scatter, bubble, mixed, radar, gauge (with gradient arc), gauge multi-ring, dual-axis (color-coded), waterfall, pareto (dual-axis), violin, calendar, funnel, rankflow, range, wordcloud, venn, sankey, graph (force-directed with optional WebGL via echarts-gl), and beeswarm (v6 jitter). Structural diagrams (org charts, C4 architecture) use purpose-built tools — see below.

---

## Structural and Architectural Diagrams

Hierarchical and architectural diagrams use purpose-built tools instead of ECharts. These are not data charts — they are structural representations with different layout, interaction, and rendering requirements.

### Organization Charts (d3-org-chart)

Interactive org hierarchy rendered client-side via d3-org-chart. Data format is a flat JSON array with parent references (`id`, `parentId`). Generated by `generate_org_chart.py`. Features: expand/collapse, zoom/pan, search, minimap, compact/expanded layout toggle, PNG/SVG export. Node template uses TL brand typography (Noto Sans) and color-coded hierarchy levels (CEO, C-suite, L2, staff, subteam).

### C4 Architecture Diagrams (D2 + astro-d2)

System context and container diagrams rendered at build time via D2's diagram language and the astro-d2 integration. Data is generated by `generate_c4_diagram.py` from AWS inventory, output as `.mdx` files with embedded D2 code blocks, processed by astro-d2 during the Astro build. Output is inline SVG with automatic dark/light theme support via D2's built-in theme system. Domain-specific color coding matches the TL categorical palette.

### Chart Type Selection — Structural Diagrams

| Chart Type | When to Use | Tool |
|---|---|---|
| Organization charts | Hierarchical people structures with 50+ nodes. Interactive expand/collapse and search are essential. | d3-org-chart |
| Architecture diagrams | System architecture, C4 context/container/component diagrams, infrastructure topology. | D2 (via astro-d2) |

---

## Accessibility for Data Visualization

### Color Independence

Color is never the sole differentiator between data series or states.

- In bar charts with status encoding, add text labels ("Pass," "Fail") in addition to color
- In line charts with multiple series, vary line dash pattern (solid, dashed, dotted) alongside color
- In scatter plots, vary marker shape (circle, square, triangle, diamond) alongside color
- In heatmaps, include the numeric value in each cell

### Contrast

- Minimum 3:1 contrast ratio for chart elements (bars, lines, points) against the chart background
- Text within charts (labels, annotations) meets 4.5:1 minimum
- Legend swatches large enough to be distinguishable (minimum 12x12px)

### Inline chart and diagram embedding

Every ECharts chart is rendered inline via `data-echarts` divs with embedded JSON. Charts include ARIA labels and decal patterns (`aria: { enabled: true, decal: { show: true } }`). D2 architecture diagrams render as inline SVG with descriptive `<title>` and `<desc>` elements. Complex diagrams (network graphs, architecture views) include an adjacent text summary — a table or narrative paragraph conveying the same insight.

### Text Alternatives

- Complex charts (network graphs, heatmaps, multi-axis comparisons) include a text summary as an adjacent HTML element — a table or narrative paragraph that conveys the same insight
- Simple charts (single-series bar, single line) may rely on the descriptive title + accessible tooltip values

### Interactive Tooltips

- `hovertemplate` includes all relevant data values: the category, the value, the unit
- Tooltip text is concise but complete — the user should not need to cross-reference another element
- Tooltips on edge/connection traces in network graphs: either `hoverinfo="skip"` (if the edge data isn't meaningful) or a clear description of the relationship

### Responsive Sizing

- Charts reflow at mobile widths — no horizontal scrolling for the chart itself
- ECharts `height: '100%', width: '100%'` with responsive `resize()` listener is always enabled
- Minimum chart height: 300px (prevents unreadable compression on small screens)
- Axis labels and legends remain legible at mobile sizes — if they don't, the chart needs a mobile-specific layout or a simpler alternate view
