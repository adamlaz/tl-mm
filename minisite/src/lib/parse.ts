/**
 * Safely coerce a string value to a number.
 * Returns 0 for undefined, empty, or non-numeric inputs.
 */
export function num(value: string | undefined): number {
  const n = parseFloat(value ?? '');
  return isNaN(n) ? 0 : n;
}

/**
 * Format a number with locale-aware thousand separators.
 * @param decimals - fixed decimal places (default 0)
 */
export function fmt(value: number, decimals = 0): string {
  return value.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/** Format a number as USD with thousand separators and no decimals. */
export function fmtCurrency(value: number): string {
  return `$${fmt(value)}`;
}
