export function formatBandwidth(bytesPerSecond: number): string {
  const mbps = (bytesPerSecond / 1024 / 1024)
  const decimal_places = mbps < 10 ? 2 : mbps < 100 ? 1 : 0
  return `${mbps.toFixed(decimal_places)}Mbps`
}
