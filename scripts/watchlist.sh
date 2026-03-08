#!/usr/bin/env bash
# watchlist.sh — Full briefing snapshot for Alain's portfolio
# Usage: bash watchlist.sh
# Compares against last saved prices in memory/watchlist-state.json

STOCKS=("CCJ" "NXE" "DNN" "URNJ" "NVDA" "BTC-USD")
COMMODITY_TICKERS=("GC=F" "SI=F" "HG=F" "CL=F")
COMMODITY_NAMES=("Gold" "Silver" "Copper" "Oil(WTI)")
STATE_FILE="$HOME/.openclaw/workspace/memory/watchlist-state.json"

# Load previous prices from state file
PREV_JSON="{}"
if [ -f "$STATE_FILE" ]; then
  PREV_JSON=$(cat "$STATE_FILE")
fi

echo "📊 Market Briefing — $(date '+%Y-%m-%d %H:%M %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STOCKS & CRYPTO"

NEW_PRICES="{}"

for TICKER in "${STOCKS[@]}"; do
  RESULT=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/${TICKER}?interval=1d&range=2d" \
    -H "User-Agent: Mozilla/5.0" 2>/dev/null)

  OUTPUT=$(echo "$RESULT" | python3 -c "
import json, sys
prev_json = '''${PREV_JSON}'''
try:
    prev_data = json.loads(prev_json).get('prices', {})
except:
    prev_data = {}
d = json.load(sys.stdin)
meta = d['chart']['result'][0]['meta']
price = meta.get('regularMarketPrice', 0)
ticker = '${TICKER}'
prev = prev_data.get(ticker, price)
chg = price - prev
pct = (chg / prev * 100) if prev else 0
arrow = '▲' if chg >= 0 else '▼'
# Mark if vs saved (not vs today's open)
label = '(vs saved)' if abs(pct) > 0 else '(no change)'
print(f'{arrow} \${price:.2f}  ({pct:+.2f}%) {label}|{price}')
" 2>/dev/null)

  if [ -n "$OUTPUT" ]; then
    DISPLAY=$(echo "$OUTPUT" | cut -d'|' -f1)
    PRICE_VAL=$(echo "$OUTPUT" | cut -d'|' -f2)
    NEW_PRICES=$(echo "$NEW_PRICES" | python3 -c "
import json, sys
d = json.load(sys.stdin)
d['${TICKER}'] = float('${PRICE_VAL}')
print(json.dumps(d))
" 2>/dev/null || echo "$NEW_PRICES")
    printf "  %-8s %s\n" "$TICKER" "$DISPLAY"
  else
    printf "  %-8s %s\n" "$TICKER" "— unavailable"
  fi
done

echo ""
echo "  COMMODITIES"

for i in "${!COMMODITY_TICKERS[@]}"; do
  TICKER="${COMMODITY_TICKERS[$i]}"
  NAME="${COMMODITY_NAMES[$i]}"
  RESULT=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/${TICKER}?interval=1d&range=2d" \
    -H "User-Agent: Mozilla/5.0" 2>/dev/null)

  OUTPUT=$(echo "$RESULT" | python3 -c "
import json, sys
prev_json = '''${PREV_JSON}'''
try:
    prev_data = json.loads(prev_json).get('prices', {})
except:
    prev_data = {}
d = json.load(sys.stdin)
meta = d['chart']['result'][0]['meta']
price = meta.get('regularMarketPrice', 0)
ticker = '${TICKER}'
prev = prev_data.get(ticker, price)
chg = price - prev
pct = (chg / prev * 100) if prev else 0
arrow = '▲' if chg >= 0 else '▼'
label = '(vs saved)' if abs(pct) > 0 else '(no change)'
print(f'{arrow} \${price:.2f}  ({pct:+.2f}%) {label}|{price}')
" 2>/dev/null)

  if [ -n "$OUTPUT" ]; then
    DISPLAY=$(echo "$OUTPUT" | cut -d'|' -f1)
    PRICE_VAL=$(echo "$OUTPUT" | cut -d'|' -f2)
    NEW_PRICES=$(echo "$NEW_PRICES" | python3 -c "
import json, sys
d = json.load(sys.stdin)
d['${TICKER}'] = float('${PRICE_VAL}')
print(json.dumps(d))
" 2>/dev/null || echo "$NEW_PRICES")
    printf "  %-10s %s\n" "$NAME" "$DISPLAY"
  else
    printf "  %-10s %s\n" "$NAME" "— unavailable"
  fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Save updated prices to state file
python3 -c "
import json, sys
from datetime import datetime, timezone
new_prices = json.loads('''${NEW_PRICES}''')
state = {'lastUpdated': datetime.now(timezone.utc).isoformat(), 'prices': new_prices}
with open('${STATE_FILE}', 'w') as f:
    json.dump(state, f, indent=2)
" 2>/dev/null

# Weather
echo "  🌤 WEATHER — Saint-Jean-sur-Richelieu"
WEATHER=$(curl -s "https://wttr.in/Saint-Jean-sur-Richelieu?format=3" 2>/dev/null)
if [ -n "$WEATHER" ]; then
  echo "  $WEATHER"
else
  echo "  (weather unavailable)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Uranium spot
echo "  ⚛️  U3O8 spot: ~\$101/lb (March 2026)"
echo ""

# Iran/Middle East news
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
