# Translation Layer — Client Deliverable Style Guide

The design system for everything Translation Layer ships to clients. Minisites, documents, slides, audio, video. This is explicitly distinct from the landing page spec ([`.impeccable.md`](.impeccable.md)) — different typefaces, different color logic, different priorities.

The governing principle: **the deliverable, the data, and the insights are the only things that matter. Translation Layer branding must not be a focus or distraction. Legibility and the ability to parse and consume are paramount.**

For how we write, see [`writing-style.md`](writing-style.md). For how data looks in charts, see [`data-visualization.md`](data-visualization.md).

---

## Philosophy

The deliverable IS the product. Not TL's brand. Not the client's brand. The data, the insights, and the audience's ability to consume them — that is all that matters.

TL proves itself through the quality and density of the deliverable, not through brand visibility. The landing page principle "craft is the argument" still holds, but in deliverables the craft is in information architecture, legibility, and visual clarity — not WebGL shaders and GSAP choreography.

The deliverable should make the client's team say "this is the clearest picture we've ever had" — not "nice branding."

---

## The Brand Relationship: TL Standard + Tactical Client Brand

This is the critical framing. TL's deliverable system is NOT white-labeled to client branding, and NOT a TL brand showcase. It is a third thing.

### TL's Own Optimized Standard

Translation Layer's own visual system governs:

- Data visualization and chart palettes
- Information architecture and layout patterns
- Document construction and typography
- Table formatting and metric displays
- Presentation style and slide structure

These are TL's instruments — precision-tuned for legibility and information density. Client brand colors are often not optimized for data-dense work: insufficient contrast ratios, poor hue separation between series, no color-blind-safe considerations, colors chosen for marketing appeal rather than analytical clarity.

Deferring to client branding for these concerns would compromise the quality of the work. A master navigator uses their own instruments — sextant, parallel rules, chronometer — regardless of which ship they're aboard.

### Client Brand Deployed Tactically

Client brand elements are included where they serve the audience:

- **Client name** in document titles, page headers, and sidebar labels
- **Client logo** in the favicon and header chrome
- **Client accent color** in navigation highlights, section accent bars, and tab indicators — places where the audience needs to feel "this is ours"

The client's people should recognize this as *their* report. But the visual system that makes it legible, parsable, and actionable is TL's.

### TL Attribution

- Footer strip: "Prepared by Translation Layer"
- The TL mark may appear in the footer at small scale, monochrome or muted
- Never: "Powered by" framing — TL is the preparer, not a platform
- The TL mark in deliverables uses the monochrome or reversed variant only, never two-tone or brass on client backgrounds

### Never in Deliverables

- Syne typography
- TL's landing page brass/steel accent palette as a deliverable color
- The Vault / Studio dark/light naming
- WebGL, particle, or motion design elements from the landing page
- Any design language that makes the deliverable look like a TL marketing piece

---

## Typography System: The Noto Superfamily

Deliverables use Google's Noto font family exclusively. The choice is deliberate: Noto is the only typeface project designed to cover every Unicode script, symbol, and emoji with visual harmony across all weights and styles. For a firm that values completeness and precision, this is the only defensible choice for information-dense, audience-specific work.

### The Family

| Face | Weights | Role |
|---|---|---|
| **Noto Sans** | 400, 500, 600, 700 | Primary body, interface, navigation. Clean, high-legibility sans-serif optimized for screen reading at all sizes. |
| **Noto Sans Display** | 400, 500, 600, 700 | Headings, section titles, hero text. Optically optimized for larger sizes where standard Noto Sans feels loose. |
| **Noto Serif** | 400, 500, 600, 700 | Long-form body text in document deliverables where serif aids sustained reading. Optional — use when the format benefits. |
| **Noto Serif Display** | 400, 500, 600, 700 | Display headings in serif-led documents. The serif counterpart to Noto Sans Display. |
| **Noto Sans Mono** | 400, 500 | Data, metrics, timelines, code, numeric table cells, technical labels. |
| **Noto Sans Symbols** | 400 | Arrows, bullets, mathematical operators, technical symbols. |
| **Noto Sans Symbols 2** | 400 | Extended symbol set: braille, chess, playing cards, transport, map symbols. |
| **Noto Emoji** | 400 | Consistent cross-platform emoji rendering. |

### Why Not Inter + JetBrains Mono?

Inter is excellent but limited to Latin, Cyrillic, and Greek scripts. JetBrains Mono is best-in-class for code editing but narrower in scope. Noto provides the same optical quality with complete Unicode coverage and a unified design language across sans, serif, mono, symbols, and emoji. One family. Total consistency. No fallback font surprises.

### Why Not Syne?

Syne is provocative and display-forward — right for the landing page where the typography IS the brand statement. Wrong for a client reading a 200-row data table at 11pm. Deliverables need typography that disappears into the content. Noto Sans achieves this.

### Type Hierarchy for Deliverables

| Role | Face | Weight | Size | Case | Tracking |
|---|---|---|---|---|---|
| Page Title | Noto Sans Display | 700 | 24–32px | Title case | −0.01em |
| Section Heading | Noto Sans Display | 600 | 18–22px | Title case | 0 |
| Sub Heading | Noto Sans | 600 | 14–16px | Title case | 0 |
| Eyebrow / Label | Noto Sans | 500 | 10–11px | Uppercase | +0.08em |
| Body | Noto Sans | 400 | 13–14px | Sentence case | 0 |
| Body (serif) | Noto Serif | 400 | 14–15px | Sentence case | 0 |
| Caption | Noto Sans | 400 | 11–12px | Sentence case | +0.02em |
| Data / Metric | Noto Sans Mono | 500 | 13–16px | As-is | 0 |
| Code / Technical | Noto Sans Mono | 400 | 12–13px | As-is | 0 |
| Table Header | Noto Sans | 500 | 11–12px | Uppercase | +0.06em |
| Table Cell (text) | Noto Sans | 400 | 12–13px | Sentence case | 0 |
| Table Cell (number) | Noto Sans Mono | 400 | 12–13px | As-is | 0 |

**Rules:** Never italic in headings. Bold (700) reserved for page titles and emphasis within body text. Monospace for all numeric data in tables, metric cards, and inline values. Display faces only at 18px and above.

---

## Color Architecture

Two-layer system: TL's own optimized palette for information and data, plus a tactical client accent for chrome and wayfinding.

### TL's Deliverable Palette

This palette is consistent across all engagements. It IS the Translation Layer deliverable standard. OKLCH-based, engineered for legibility.

**Warm Neutrals** (backgrounds and text, extending TL's hue ~80/~300 warmth):

| Token | Light Mode | Dark Mode | Role |
|---|---|---|---|
| `--bg` | `oklch(97.5% 0.002 80)` | `oklch(13% 0.015 300)` | Page background |
| `--surface` | `oklch(100% 0 0)` | `oklch(18% 0.015 300)` | Card / component surface |
| `--surface-alt` | `oklch(93% 0.003 80)` | `oklch(26% 0.012 300)` | Alternate surface, table stripes |
| `--text` | `oklch(18% 0.015 300)` | `oklch(93% 0.003 80)` | Primary text |
| `--text-secondary` | `oklch(36% 0.008 300)` | `oklch(76% 0.004 80)` | Secondary text, descriptions |
| `--text-muted` | `oklch(46% 0.006 300)` | `oklch(66% 0.004 80)` | Tertiary text, captions, labels |

**Cool Structural Steel** (borders, dividers, secondary elements, hue ~250):

| Token | Light Mode | Dark Mode | Role |
|---|---|---|---|
| `--border` | `oklch(86% 0.003 250)` | `oklch(36% 0.008 250)` | Primary border |
| `--border-subtle` | `oklch(93% 0.003 250)` | `oklch(26% 0.012 250)` | Subtle dividers, grid lines |
| `--ring` | `oklch(62% 0.12 250)` | `oklch(62% 0.12 250)` | Focus indicators |

**Status Colors** (fixed, decoupled from any accent):

| Token | Value | Usage |
|---|---|---|
| `--status-green` | `oklch(65% 0.17 145)` | Healthy, pass, on-track |
| `--status-amber` | `oklch(75% 0.15 75)` | Warning, degraded, at-risk |
| `--status-red` | `oklch(60% 0.2 25)` | Critical, fail, blocked |
| `--status-green-bg` | `oklch(95% 0.04 145)` | Green background tint |
| `--status-amber-bg` | `oklch(95% 0.04 75)` | Amber background tint |
| `--status-red-bg` | `oklch(95% 0.04 25)` | Red background tint |

### Client Accent Layer

Deployed tactically. The only token that changes per engagement.

**Process:** Extract the client's primary brand hue. Build a 3-stop OKLCH scale:

| Token | Construction | Usage |
|---|---|---|
| `--accent` | Client hue, ~55% lightness, moderate chroma | Navigation active states, header accent bar, section markers |
| `--accent-hover` | Client hue, ~45% lightness, slightly higher chroma | Hover/focus states on accent elements |
| `--accent-subtle` | Client hue, ~95% lightness, low chroma | Accent background tints, active tab backgrounds |

The client accent is sufficient for UI chrome — navigation highlights, header bars, favicon. It is NOT used in data visualization, table formatting, status indicators, or body text. Those are governed by TL's own palette.

### Semantic Token Architecture

All deliverables share the same token names. Only the primitive values change.

```css
:root {
  --bg: /* TL standard warm neutral */;
  --surface: /* TL standard */;
  --surface-alt: /* TL standard */;
  --text: /* TL standard */;
  --text-secondary: /* TL standard */;
  --text-muted: /* TL standard */;
  --border: /* TL standard steel */;
  --border-subtle: /* TL standard steel */;
  --ring: /* TL standard steel */;
  --accent: /* client-derived */;
  --accent-hover: /* client-derived */;
  --accent-subtle: /* client-derived */;
}
```

Light mode is the default. Dark mode is supported via `[data-theme="dark"]`. Both are fully designed — dark mode is not an afterthought.

---

## Layout Patterns

Codified from the mm-engagement minisite and generalized for reuse.

### Page Shell

- **Desktop:** Fixed left sidebar (~`w-56`) with navigation, scrollable main content column, sticky header strip, confidentiality footer strip.
- **Mobile:** Sidebar hidden. Bottom tab bar for primary navigation (subset of routes). Hamburger for full nav if needed.
- **Header strip:** Client name, engagement title, date. Sticky. Subtle border-bottom.
- **Footer strip:** "Prepared by Translation Layer" on the left. "Confidential" on the right. Always present.

### Navigation Structure

Group by domain or concern, not by document type:

- **Overview** (Dashboard, Engagement Context)
- **Systems** (Infrastructure, Engineering, Delivery, Documentation)
- **Cross-Cutting** (People & Org, Tooling, Surveys)
- **Reference** (Charts, Data Tables, Appendices)

### Content Patterns

- **Metric card grids:** `grid-cols-2 lg:grid-cols-4` for dashboard KPIs. Each card: value (Noto Sans Mono, large), label (Noto Sans, small caps), optional delta/trend indicator.
- **Section headers:** Eyebrow label (uppercase, small, muted) + title (Noto Sans Display 600) + optional description paragraph.
- **Data tables:** Sortable columns. Noto Sans Mono for all numeric cells. Noto Sans for text cells. Striped rows or hover highlights for scannability. Table headers in uppercase with tracking.
- **Chart embeds:** Inline `data-echarts` divs with embedded JSON. Scroll-triggered rendering. Optional fullscreen and caption below.
- **Finding cards:** Severity-colored left border (red/amber/green from status palette). Hypothesis ID. Evidence summary. Linked metric references.
- **Key findings blocks:** Prominent placement on dashboard. Each finding with a severity-coded border and a 1–2 sentence summary. Links to the relevant detail section.

### Spacing System

Base unit: 4px. Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80.

- Section padding: 48–64px vertical
- Card padding: 16–20px
- Grid gap: 8–12px between cards
- Component internal spacing: 8–16px

---

## Component Conventions

Reusable patterns across all deliverable types. Named for clarity, not for a component library.

### MetricCard

- Value: Noto Sans Mono 500, 24–32px, `--text`
- Label: Noto Sans 500, 10–11px, uppercase, +0.08em tracking, `--text-muted`
- Optional delta: small arrow + percentage, green/red from status palette
- Container: `--surface`, `--border` border, rounded corners (8–12px)

### DataTable

- Implementation: Tabulator (tabulator-tables v6) with TL CSS theming
- Features: sorting, filtering, search, pagination, row grouping, conditional formatting, CSV export, frozen columns, responsive layout
- Header row: Noto Sans 500, 11px, uppercase, `--text-muted`, border-bottom
- Text cells: Noto Sans 400, 12–13px, `--text`
- Number cells: Noto Sans Mono 400, 12–13px, `--text`
- First column (label): Noto Sans 500, `--accent` or `--text` depending on context
- Alternating row tint: `--surface-alt`
- Sort indicators: arrows in `--text-muted`

### ChartEmbed

- Wrapper: rounded card with header, optional fullscreen button
- Implementation: inline `data-echarts` div with chart data embedded via `<script type="application/json">`
- Rendering: scroll-triggered via IntersectionObserver, canvas renderer with `useDirtyRect` optimization
- Dark mode: `MutationObserver` on `data-theme` attribute, dispose/reinit with `tl-dark` theme
- ARIA: `aria: { enabled: true, decal: { show: true } }` on every chart
- Toolbox: save-as-PNG, data view, reset zoom on every chart
- Optional interactive hint: "Scroll to zoom · Drag to pan"
- See [`data-visualization.md`](data-visualization.md) for chart-internal styling

### OrgChart

- Implementation: d3-org-chart with custom TL node template
- Features: expand/collapse, zoom/pan, search, minimap, compact/expanded toggle, PNG/SVG export
- Node card: color-coded left stripe by hierarchy level (CEO, C-suite, L2, staff, subteam), Noto Sans 600 for name, Noto Sans 400 for role, headcount badge, division tag
- Dark mode: CSS custom properties, re-render on theme change via MutationObserver
- Container: `--surface`, `--border` border, rounded corners, toolbar row above chart with search input and layout controls

### D2Diagram

- Implementation: D2 source processed by astro-d2 at Astro build time, output as inline SVG
- Features: responsive SVG sizing, automatic dark/light theme via D2 theme configuration
- Styling: domain-specific fill colors from TL categorical palette
- Container: `--surface`, `--border` border, rounded corners, title header with source attribution

### StatusBadge

- Colors from TL's fixed status palette — never client-derived
- Emerald (healthy/pass), Amber (warning/at-risk), Red (critical/fail)
- Pill shape: small text (10–11px), uppercase, background tint + text color from status tokens
- Optional icon/emoji prefix for additional clarity

### SectionHeader

- Eyebrow: Noto Sans 500, 10px, uppercase, `--text-muted`, +0.08em tracking
- Title: Noto Sans Display 600, 20–24px, `--text`
- Description: Noto Sans 400, 13px, `--text-secondary`, max-width 640px

### FindingCard

- Left border: 3px solid, color from status palette
- Hypothesis ID: Noto Sans Mono 500, small, `--text-muted`
- Title: Noto Sans 600, 14px, `--text`
- Evidence summary: Noto Sans 400, 13px, `--text-secondary`
- Linked metrics or chart references as inline links

---

## Emoji, Icon, and Symbol Integration

Noto Emoji and Noto Sans Symbols are first-class deliverable tools, not afterthoughts.

### Appropriate Uses

- Status indicators in metric cards and tables (health, severity, progress)
- Category markers in dense lists that benefit from visual grouping
- Severity encoding in finding cards alongside colored borders
- Navigation icons in sidebar and tab bar
- Inline data annotations in chart tooltips

### The Standard

The Noto family guarantees visual consistency. A status emoji in a chart tooltip renders identically on macOS, Windows, Linux, and mobile. This eliminates the cross-platform rendering inconsistencies that plague OS-native emoji.

Symbols and arrows from Noto Sans Symbols replace icon libraries in most cases. Fewer dependencies, consistent weight with body text, no icon font loading latency.

### The Rule

Use emoji/symbols when they are the fastest path to comprehension. Never to soften language, add false warmth, or substitute for clear writing. If removing the symbol makes the content no harder to parse, remove it.

---

## Deliverable Type Specifications

### Minisites

**Stack:** Astro + Tailwind CSS v4 + @astrojs/mdx + astro-d2. Noto fonts via Google Fonts. Vercel deployment.

**Structure:**
- `src/layouts/BaseLayout.astro` — page shell with header, sidebar, footer, theme script
- `src/styles/global.css` — Tailwind `@theme` with TL deliverable tokens + semantic variables
- `src/components/` — reusable patterns (MetricCard, DataTable, ChartEmbed, StatusBadge, SectionHeader)
- `src/pages/` — one page per major section/domain
- `analysis/charts/*.json` — ECharts v6 JSON consumed inline by data-echarts components
- `src/content.config.ts` — data collections from CSV/JSON (sibling analysis directories)

**Conventions:**
- Sidebar navigation grouped by domain
- View transitions for smooth page-to-page navigation
- `prefers-reduced-motion` respected
- Chart assets generated by Python scripts: ECharts v6 JSON for data charts (inline rendering), D2 source in MDX for architecture diagrams (build-time SVG via astro-d2), flat JSON for org charts (d3-org-chart client-side rendering). Data tables rendered via Tabulator.
- Data pipeline: `scripts/` generates `analysis/` artifacts, minisite reads them

### Documents

**Format:** Structured markdown.

**Conventions:**
- Title, audience, author, date, and confidentiality level in the header
- Version number and changelog ("What's Changed in v12") when iterating
- "Working Draft" vs. "Final" distinction in the header
- Tables for timelines, specifications, role assignments, action items
- Action items with named owners and hard dates
- "What this is / what it isn't" framing when introducing new work to anxious audiences
- Explicit tiering: Core (guaranteed), Expected (high confidence), Stretch (if time allows)
- `[PRIVATE]` tags for sensitive observations that stay between principals

### Slides

**Generated via:** NotebookLM or manual construction.

**Conventions:**
- Headline + bullets, never paragraphs on a slide
- Maximum 6 bullets per slide — if more, split
- High contrast: dark text on light ground or light text on dark ground
- Strong typography: Noto Sans Display for headlines, Noto Sans for bullets
- No clip art, no generic icons, no stock photography
- Table or timeline visual for structured data (not bullet lists)
- "Not a sales deck. An operational briefing between people who are about to work together."
- Title slide: Engagement name, client name, preparer, date, "Confidential"

### Audio

**Generated via:** NotebookLM or podcast-style recording.

**Conventions:**
- Conversational, direct, peer-to-peer tone
- Target 8–12 minutes — orientation, not exhaustive walkthrough
- "Like three experienced engineers talking about how to run a good assessment"
- Enthusiastic but grounded — not hype, not doom
- Structure around themes, not slide-by-slide narration
- Do NOT speculate about findings. Do NOT discuss compensation, investor dynamics, or politics.
- Treat every named individual as a respected partner

### Video

**Generated via:** NotebookLM or professional production.

**Conventions:**
- "Executive briefing deck that moves"
- Low text density per frame
- Visual emphasis on structure, data, and organizational patterns
- Confident pace, not rushed
- Same content guardrails as audio: no speculation, no politics, no compensation

---

## Accessibility

Non-negotiable. Accessibility is evidence of craft, not a compliance checkbox.

### Standards

- **WCAG 2.1 AA** minimum. AAA where practical.
- `prefers-reduced-motion` respected in all view transitions and animations
- Focus indicators (`--ring` token, 2px solid, 2px offset) on all interactive elements
- Keyboard navigation complete — every interaction reachable without a mouse
- Skip-to-content link on every page
- Semantic HTML: `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `<table>` with proper `<thead>`/`<tbody>`

### Color

- Color is never the sole carrier of meaning — pair with text labels, icons, or patterns
- Status colors (green/amber/red) always accompanied by text or icon
- Minimum 4.5:1 contrast ratio for body text
- Minimum 3:1 contrast ratio for large text, UI components, and graphical objects

### Charts

- Every chart has ARIA labels and decal patterns for accessibility
- Complex charts include a text summary (table or narrative) as an adjacent alternative
- Interactive tooltips include all relevant data values
- See [`data-visualization.md`](data-visualization.md) for full chart accessibility requirements

### Responsive

- Sidebar collapses to bottom tab bar on mobile
- No information loss at mobile widths — content reflows, tables scroll horizontally
- Touch targets minimum 44x44px on mobile
- Font sizes respect user preferences — use `rem` units, not fixed `px` for body text

---

## Information Density Standards

Legibility over beauty. Density over decoration. Every visual element serves comprehension.

- **Minimum body text:** 13px. No 10px body copy in any context.
- **Metric values:** Always Noto Sans Mono. Consistent alignment, tabular figures.
- **Tables over prose:** If data has a natural row/column structure, use a table.
- **Content-first:** No decorative elements that don't serve comprehension. No background patterns, gradient overlays, or ornamental dividers.
- **Whitespace is structure:** Use generous whitespace between sections to create scannable rhythm. Cramped pages are as hard to read as cluttered ones.
- **Progressive depth:** Dashboard summaries link to section detail. Section detail links to raw data. The reader chooses their depth.
