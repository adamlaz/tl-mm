import { parse } from 'csv-parse/sync';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { Loader } from 'astro/loaders';

export interface CsvLoaderOptions {
  path: string;
  idColumn?: string;
}

export function csvLoader(opts: CsvLoaderOptions): Loader {
  return {
    name: 'csv-loader',
    async load({ store, logger, parseData }) {
      const abs = resolve(opts.path);
      const raw = readFileSync(abs, 'utf-8');
      const records: Record<string, string>[] = parse(raw, {
        columns: true,
        skip_empty_lines: true,
        relax_column_count: true,
      });
      logger.info(`Loaded ${records.length} rows from ${opts.path}`);
      store.clear();
      for (const [i, row] of records.entries()) {
        const id = opts.idColumn ? (row[opts.idColumn] ?? String(i)) : String(i);
        const data = await parseData({ id, data: row });
        store.set({ id, data });
      }
    },
  };
}
