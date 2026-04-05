/**
 * TL Tabulator Formatter Library
 * Reusable cell formatters matching the Translation Layer deliverable standard.
 * Uses the TL categorical palette (data-visualization.md) and status colors
 * (client-deliverable-style.md).
 *
 * Exported as serializable config objects that the TabulatorGrid client script
 * reconstructs into live formatter functions.
 */

const CAT_CLASSES = [
  'tl-cat-0', 'tl-cat-1', 'tl-cat-2', 'tl-cat-3',
  'tl-cat-4', 'tl-cat-5', 'tl-cat-6', 'tl-cat-7',
];

const STATUS_MAP: Record<string, string> = {
  green: 'tl-st-green',
  amber: 'tl-st-amber',
  red: 'tl-st-red',
  muted: 'tl-st-muted',
  accent: 'tl-st-accent',
};

const SEQUENTIAL_LIGHT = ['#E8EEF5', '#C0DCD8', '#E0D498', '#D0A040', '#C06030', '#902820'];
const SEQUENTIAL_DARK = ['#18202A', '#1A2E2C', '#2E2814', '#50401A', '#704020', '#E0A060'];

export function catHash(s: string): number {
  let v = 5381;
  const str = String(s || '').toLowerCase().trim();
  for (let i = 0; i < str.length; i++) v = ((v << 5) + v) + str.charCodeAt(i);
  return Math.abs(v) % 8;
}

export function catClass(val: string, badgeMap?: Record<string, string> | null): string {
  const s = String(val);
  const mapped = badgeMap ? (badgeMap[s] || badgeMap[s.toLowerCase()]) : null;
  if (mapped && STATUS_MAP[mapped]) return STATUS_MAP[mapped];
  return CAT_CLASSES[catHash(s)];
}

export function initials(name: string): string {
  const parts = String(name || '').split(/\s+/).filter(Boolean);
  if (!parts.length) return '?';
  return parts.length === 1
    ? parts[0][0].toUpperCase()
    : (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function parseNum(v: any): number {
  return parseFloat(String(v || '0').replace(/[^0-9.\-]/g, '')) || 0;
}

function wrapLink(html: string, href: string): string {
  if (!href) return html;
  const ext = String(href).startsWith('http');
  const attrs = ext ? ' target="_blank" rel="noopener noreferrer"' : '';
  const arrow = ext ? '<span class="tl-ext-arrow">\u2197</span>' : '';
  return `<a class="tl-cell-link" href="${href}"${attrs}>${html}${arrow}</a>`;
}

// ─── Formatter builders ───
// These return HTML strings. Used by TabulatorGrid's client script.

export function badgeHTML(val: any, badgeMap?: Record<string, string> | null, href?: string): string {
  if (!val && val !== 0) return '';
  const s = String(val);
  const cls = catClass(val, badgeMap);
  let out = `<span class="tl-badge ${cls}">${s}</span>`;
  if (href) out = wrapLink(out, href);
  return out;
}

export function barHTML(val: any, max = 100, invert = false): string {
  if (val === '' || val === null || val === undefined) return '';
  const n = parseNum(val);
  const pct = Math.min(100, Math.max(0, (n / (max > 0 ? max : 100)) * 100));
  let cl: string;
  if (invert) {
    cl = pct <= 40 ? 'tl-bar--green' : pct <= 70 ? 'tl-bar--amber' : 'tl-bar--red';
  } else {
    cl = pct <= 40 ? 'tl-bar--red' : pct <= 70 ? 'tl-bar--amber' : 'tl-bar--green';
  }
  return `<div class="tl-bar-wrap"><span class="tl-bar-label">${val}</span><div class="tl-bar-track"><div class="tl-bar-fill ${cl}" style="width:${pct}%"></div></div></div>`;
}

export function avatarHTML(val: any, subtitle?: string, href?: string): string {
  if (!val) return '';
  const ini = initials(val as string);
  const cls = CAT_CLASSES[catHash(val as string)];
  let nm = `<span class="tl-avatar-name">${val}</span>`;
  if (href) nm = wrapLink(nm, href);
  const sub = subtitle ? `<div class="tl-avatar-sub">${subtitle}</div>` : '';
  return `<div class="tl-avatar-cell"><div class="tl-avatar-circle ${cls}">${ini}</div><div>${nm}${sub}</div></div>`;
}

export function booleanHTML(val: any): string {
  const s = String(val || '').toLowerCase().trim();
  const yes = s === 'yes' || s === 'true' || s === '1' || s === 'active' || s === 'enabled';
  if (yes) return `<span class="tl-bool tl-bool--yes"><span class="tl-bool-icon">\u2713</span>${val}</span>`;
  return `<span class="tl-bool tl-bool--no"><span class="tl-bool-icon">\u2014</span>${val}</span>`;
}

export function currencyHTML(val: any): string {
  if (!val && val !== 0) return '';
  return `<span class="tl-currency">${val}</span>`;
}

export function listHTML(val: any): string {
  if (!val) return '';
  return String(val)
    .split(/,\s*/)
    .map((item) => `<span class="tl-list-pill ${CAT_CLASSES[catHash(item)]}">${item.trim()}</span>`)
    .join(' ');
}

export function linkHTML(val: any, href?: string): string {
  if (!val) return '';
  if (!href) return String(val);
  return wrapLink(String(val), href);
}

export function dateHTML(val: any): string {
  if (!val) return '';
  return `<span style="white-space:nowrap">${val}</span>`;
}

export function heatHTML(val: any, max = 100, isDark = false): string {
  if (val === '' || val === null || val === undefined) return '';
  const n = parseNum(val);
  const norm = Math.min(1, Math.max(0, n / (max > 0 ? max : 100)));
  const palette = isDark ? SEQUENTIAL_DARK : SEQUENTIAL_LIGHT;
  const idx = Math.min(palette.length - 1, Math.floor(norm * (palette.length - 1)));
  const bg = palette[idx];
  const fg = norm > 0.5 ? (isDark ? '#1E1810' : '#FFF6EE') : (isDark ? '#90A0B0' : '#404860');
  return `<span class="tl-heat-cell" style="background:${bg};color:${fg}">${val}</span>`;
}

export function sparklineHTML(values: number[], max?: number): string {
  if (!values || !values.length) return '';
  const m = max || Math.max(...values, 1);
  const colors = ['#5A6CD0', '#2AA89A', '#C4A030', '#D05848', '#6A80B8'];
  return `<span class="tl-spark">${values.map((v, i) => {
    const h = Math.max(2, Math.round((v / m) * 18));
    return `<span class="tl-spark-seg" style="height:${h}px;background:${colors[i % colors.length]}"></span>`;
  }).join('')}</span>`;
}
