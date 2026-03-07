#!/usr/bin/env bash
# watchlist.sh — Full briefing snapshot for Alain's portfolio
# Usage: bash watchlist.sh

STOCKS=("CCJ" "NXE" "DNN" "URNJ" "NVDA" "BTC-USD")
COMMODITIES=("GC=F" "SI=F" "HG=F" "CL=F")
COMMODITY_NAMES=("Gold" "Silver" "Copper" "Oil(WTI)")

echo "📊 Market Briefing — $(date '+%Y-%m-%d %H:%M %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STOCKS & CRYPTO"

for TICKER in "${STOCKS[@]}"; do
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

echo ""
echo "  COMMODITIES"

for i in "${!COMMODITIES[@]}"; do
  TICKER="${COMMODITIES[$i]}"
  NAME="${COMMODITY_NAMES[$i]}"
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

  printf "  %-10s %s\n" "$NAME" "$PRICE"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  U3O8 spot: ~\$101/lb (March 2026)"
echo ""
echo "  🌍 IRAN/MIDDLE EAST — Latest Headlines"
curl -s "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml" | python3 -c "
import sys, xml.etree.ElementTree as ET
content = sys.stdin.read()
root = ET.fromstring(content)
items = root.findall('.//item')[:3]
for item in items:
    title = item.find('title')
    pubdate = item.find('pubDate')
    if title is not None:
        print(f'  • {title.text[:85]}')
        if pubdate is not None:
            print(f'    ({pubdate.text[:25]})')
" 2>/dev/null || echo "  (news unavailable)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
