export function num(value: string | undefined): number {
  const n = parseFloat(value ?? '');
  return isNaN(n) ? 0 : n;
}

export function fmt(value: number, decimals = 0): string {
  return value.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

export function fmtCurrency(value: number): string {
  return `$${fmt(value)}`;
}
