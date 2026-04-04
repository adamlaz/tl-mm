import { parse } from 'csv-parse/sync';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { Loader } from 'astro/loaders';

export interface CsvLoaderOptions {
  /** Path to the CSV file, resolved relative to the minisite root. */
  path: string;
  /** Column to use as the entry ID. Falls back to row index when omitted. */
  idColumn?: string;
}

/**
 * Astro content loader that reads a CSV file at build time and yields
 * one collection entry per row.
 */
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
