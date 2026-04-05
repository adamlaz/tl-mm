/**
 * ECharts inline initialization runtime.
 *
 * Single module that owns all chart lifecycle: theme registration,
 * IntersectionObserver scroll-trigger, dark mode via MutationObserver,
 * prefers-reduced-motion, resize, dispose on View Transition page swap,
 * and JS-function post-processing for bubble/wordcloud charts.
 */

declare const echarts: any;

const TL_CATEGORICAL = [
  '#4A5FC4', '#2A9D8F', '#C4973A', '#C4574A',
  '#6B82A0', '#6FAA5C', '#9A6B9A', '#B07A4A',
];

const TL_DARK_THEME = {
  backgroundColor: '#1E1A1A',
  textStyle: { color: '#E8E4DE' },
  title: {
    textStyle: { color: '#E8E4DE' },
    subtextStyle: { color: '#8A8070' },
  },
  legend: { textStyle: { color: '#B0A890' } },
  tooltip: {
    backgroundColor: '#1E1A1A',
    borderColor: '#4A4038',
    textStyle: { color: '#E8E4DE' },
  },
  categoryAxis: {
    axisLine: { lineStyle: { color: '#4A4038' } },
    axisTick: { lineStyle: { color: '#4A4038' } },
    axisLabel: { color: '#8A8070' },
    splitLine: { lineStyle: { color: '#3A3430' } },
  },
  valueAxis: {
    axisLine: { lineStyle: { color: '#4A4038' } },
    axisTick: { lineStyle: { color: '#4A4038' } },
    axisLabel: { color: '#8A8070' },
    splitLine: { lineStyle: { color: '#3A3430' } },
  },
  color: ['#6B7FE0', '#3AC4B4', '#D4A74A', '#D46A5A', '#8A9EC0', '#8ACC7A', '#B48AB4', '#C89060'],
};

interface ChartEntry {
  chart: any;
  option: any;
}

const instances = new Map<HTMLElement, ChartEntry>();
let themeRegistered = false;

function currentTheme(): string | null {
  return document.documentElement.getAttribute('data-theme') === 'dark' ? 'tl-dark' : null;
}

function applyPostProcessing(option: any, meta: any) {
  if (meta.bubble) {
    for (const s of option.series || []) {
      if (s.symbolSize === '__BUBBLE__') {
        s.symbolSize = (v: any) => {
          const d = Array.isArray(v) ? v : [];
          return Math.max(5, Math.min(40, Math.sqrt(d[2] || 0) * 3));
        };
      }
    }
  }
  if (meta.wordcloud) {
    const colors = [...TL_CATEGORICAL];
    for (const s of option.series || []) {
      if (s.textStyle?.color === '__WORDCLOUD_COLOR__') {
        s.textStyle.color = () => colors[Math.floor(Math.random() * colors.length)];
      }
    }
  }
}

function disableAnimation(option: any) {
  option.animation = false;
  for (const s of option.series || []) {
    s.animation = false;
    if (s.detail) s.detail.valueAnimation = false;
  }
}

function renderChart(el: HTMLElement, option: any) {
  const chart = echarts.init(el, currentTheme(), {
    renderer: 'canvas',
    useDirtyRect: true,
  });
  chart.setOption(option);
  (el as any).__echart = chart;
  instances.set(el, { chart, option });
}

function initCharts() {
  if (typeof echarts === 'undefined') return;

  if (!themeRegistered) {
    echarts.registerTheme('tl-dark', TL_DARK_THEME);
    themeRegistered = true;
  }

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const divs = document.querySelectorAll<HTMLElement>('[data-echarts]');

  divs.forEach((el) => {
    if (instances.has(el)) return;
    const script = el.querySelector('script[type="application/json"]');
    if (!script?.textContent) return;

    let parsed: any;
    try {
      parsed = JSON.parse(script.textContent);
    } catch {
      return;
    }

    const meta = parsed._meta || {};
    const option = parsed.option || parsed;
    applyPostProcessing(option, meta);

    if (option.aria?.decal) {
      option.aria.decal.show = false;
    }

    if (reducedMotion) {
      disableAnimation(option);
      renderChart(el, option);
    } else {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            renderChart(el, option);
            observer.disconnect();
          }
        },
        { threshold: 0.15 },
      );
      observer.observe(el);
    }
  });
}

function disposeAll() {
  instances.forEach(({ chart }, el) => {
    try { chart.dispose(); } catch {}
    (el as any).__echart = undefined;
  });
  instances.clear();
}

function onThemeChange() {
  instances.forEach(({ chart, option }, el) => {
    try { chart.dispose(); } catch {}

    const newChart = echarts.init(el, currentTheme(), {
      renderer: 'canvas',
      useDirtyRect: true,
    });
    newChart.setOption(option);
    (el as any).__echart = newChart;
    instances.set(el, { chart: newChart, option });
  });
}

// -- Lifecycle: Astro View Transitions ---------------------------------
document.addEventListener('astro:page-load', initCharts);
document.addEventListener('astro:before-swap', disposeAll);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCharts);
} else {
  initCharts();
}

// -- Dark mode: observe data-theme attribute changes -------------------
new MutationObserver(onThemeChange).observe(document.documentElement, {
  attributes: true,
  attributeFilter: ['data-theme'],
});

// -- Resize: debounced -------------------------------------------------
let resizeTimer: number;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(() => {
    instances.forEach(({ chart }) => chart.resize());
  }, 100);
});
