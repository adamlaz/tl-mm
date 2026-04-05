/**
 * The @astrojs/vercel adapter places "handle": "filesystem" before middleware
 * in the Build Output config, so prerendered static pages bypass Edge Middleware.
 * This script injects a middleware route before the filesystem handler, ensuring
 * the auth middleware runs for every request.
 */
import { readFileSync, writeFileSync } from 'node:fs';

const configPath = '.vercel/output/config.json';
const config = JSON.parse(readFileSync(configPath, 'utf-8'));

const middlewareRoute = { src: '/.*', middlewarePath: '_middleware', continue: true };
const hasMiddlewareRoute = config.routes?.some((r) => r.middlewarePath === '_middleware');

if (!hasMiddlewareRoute) {
  config.routes.unshift(middlewareRoute);
  writeFileSync(configPath, JSON.stringify(config, null, '\t') + '\n');
  console.log('[patch] Injected Edge Middleware route before filesystem handler');
} else {
  console.log('[patch] Middleware route already present, skipping');
}
