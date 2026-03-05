#!/usr/bin/env bash
# watchlist.sh — Quick price snapshot for Alain's portfolio
# Usage: bash watchlist.sh

TICKERS=("CCJ" "NXE" "DNN" "URNJ" "NVDA" "BTC-USD")

echo "📊 Watchlist Snapshot — $(date '+%Y-%m-%d %H:%M %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for TICKER in "${TICKERS[@]}"; do
  RESULT=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/${TICKER}?interval=1d&range=2d" \
    -H "User-Agent: Mozilla/5.0" 2>/dev/null)

  PRICE=$(echo "$RESULT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
meta = d['chart']['result'][0]['meta']
price = meta.get('regularMarketPrice', 0)
prev = meta.get('previousClose', price)
chg = price - prev
pct = (chg / prev * 100) if prev else 0
arrow = '▲' if chg >= 0 else '▼'
print(f\"{arrow} \${price:.2f}  ({pct:+.2f}%)\")
" 2>/dev/null || echo "  — unavailable")

  printf "  %-8s %s\n" "$TICKER" "$PRICE"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  U3O8 spot: ~\$101/lb (March 2026)"
