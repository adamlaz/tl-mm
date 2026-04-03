import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { Loader } from 'astro/loaders';

export interface JsonExtractLoaderOptions {
  path: string;
  key: string;
  idField?: string;
}

export function jsonExtractLoader(opts: JsonExtractLoaderOptions): Loader {
  return {
    name: 'json-extract-loader',
    async load({ store, logger, parseData }) {
      const abs = resolve(opts.path);
      const raw = JSON.parse(readFileSync(abs, 'utf-8'));
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const items: any[] = opts.key.split('.').reduce((o: any, k: string) => o[k], raw);
      logger.info(`Loaded ${items.length} items from ${opts.path} [${opts.key}]`);
      store.clear();
      for (const [i, item] of items.entries()) {
        const id = String(item[opts.idField ?? 'id'] ?? i);
        const data = await parseData({ id, data: item });
        store.set({ id, data });
      }
    },
  };
}
