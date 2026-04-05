import { defineMiddleware } from 'astro:middleware';

const SECURITY_HEADERS: Record<string, string> = {
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'X-Robots-Tag': 'noindex, nofollow',
  'X-Middleware': 'active',
};

function addSecurityHeaders(response: Response): Response {
  const newResponse = new Response(response.body, response);
  for (const [key, value] of Object.entries(SECURITY_HEADERS)) {
    newResponse.headers.set(key, value);
  }
  return newResponse;
}

function unauthorizedResponse(): Response {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Authentication Required | Mad Mobile Engagement</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600&family=Noto+Sans+Display:wght@600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: oklch(97.5% 0.002 80);
      --text: oklch(18% 0.015 300);
      --text-secondary: oklch(36% 0.008 300);
      --text-muted: oklch(46% 0.006 300);
      --border: oklch(86% 0.003 250);
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: oklch(13% 0.015 300);
        --text: oklch(93% 0.003 80);
        --text-secondary: oklch(76% 0.004 80);
        --text-muted: oklch(66% 0.004 80);
        --border: oklch(36% 0.008 250);
      }
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Noto Sans', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      -webkit-font-smoothing: antialiased;
    }
    main { text-align: center; padding: 2rem; max-width: 400px; }
    .mark { width: 40px; height: 40px; margin: 0 auto 1.5rem; color: var(--text-muted); }
    h1 {
      font-family: 'Noto Sans Display', 'Noto Sans', system-ui, sans-serif;
      font-weight: 600; font-size: 20px; letter-spacing: -0.01em; margin-bottom: 0.75rem;
    }
    p { font-size: 13px; line-height: 1.6; color: var(--text-secondary); }
    footer {
      position: fixed; bottom: 0; left: 0; right: 0;
      border-top: 1px solid var(--border); padding: 0.625rem 1.5rem;
      display: flex; align-items: center; justify-content: space-between;
      font-size: 11px; color: var(--text-muted);
    }
    footer .tl { font-weight: 500; }
  </style>
</head>
<body>
  <main>
    <svg class="mark" viewBox="0 0 100 100" fill="none" stroke="currentColor" aria-hidden="true">
      <path d="M 65.75,33.21 A 29 29 0 0 1 33.21,65.75" stroke-width="2.2"/>
      <path d="M 66.79,65.75 A 29 29 0 0 1 34.25,33.21" stroke-width="1.4" stroke-dasharray="2 2.5"/>
      <path d="M 33.21,34.25 A 29 29 0 0 1 65.75,66.79" stroke-width="1.5" stroke-dasharray="7 3"/>
      <path d="M 34.25,66.79 A 29 29 0 0 1 66.79,34.25" stroke-width="1" stroke-dasharray="1.5 2.5"/>
    </svg>
    <h1>Authentication Required</h1>
    <p>This site contains confidential engagement materials. Enter your credentials to continue.</p>
  </main>
  <footer>
    <span>Prepared by <span class="tl">Translation Layer</span></span>
    <span>Confidential</span>
  </footer>
</body>
</html>`;

  return new Response(html, {
    status: 401,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'WWW-Authenticate': 'Basic realm="Mad Mobile Engagement"',
      'Cache-Control': 'no-store',
      ...SECURITY_HEADERS,
    },
  });
}

export const onRequest = defineMiddleware(async (context, next) => {
  // Astro dev server passes empty headers to middleware for prerendered pages,
  // so auth can only be tested via `npm run preview` or on Vercel.
  if (import.meta.env.DEV) {
    return addSecurityHeaders(await next());
  }

  const user = process.env.SITE_USER;
  const password = process.env.SITE_PASSWORD;

  if (!user || !password) {
    return addSecurityHeaders(await next());
  }

  const authorization = context.request.headers.get('authorization');
  if (authorization) {
    const [scheme, encoded] = authorization.split(' ');
    if (scheme === 'Basic' && encoded) {
      const decoded = atob(encoded);
      const idx = decoded.indexOf(':');
      if (idx !== -1 && decoded.slice(0, idx) === user && decoded.slice(idx + 1) === password) {
        return addSecurityHeaders(await next());
      }
    }
  }

  return unauthorizedResponse();
});
