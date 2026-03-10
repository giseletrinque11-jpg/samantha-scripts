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

# Weather — Open-Meteo API (Saint-Jean-sur-Richelieu: 45.3089, -73.2659)
echo "  🌤 WEATHER — Saint-Jean-sur-Richelieu"
WEATHER_RAW=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=45.3089&longitude=-73.2659&current=temperature_2m,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code&forecast_days=2&timezone=America%2FToronto" 2>/dev/null)
if [ -n "$WEATHER_RAW" ]; then
  python3 -c "
import json, sys
d = json.loads('''${WEATHER_RAW}''')
wc = {0:'☀️ Clear',1:'🌤 Mostly clear',2:'⛅ Partly cloudy',3:'☁️ Overcast',45:'🌫 Foggy',48:'🌫 Icy fog',51:'🌦 Light drizzle',53:'🌦 Drizzle',55:'🌧 Heavy drizzle',61:'🌧 Light rain',63:'🌧 Rain',65:'🌧 Heavy rain',71:'🌨 Light snow',73:'🌨 Snow',75:'❄️ Heavy snow',80:'🌦 Showers',81:'🌧 Heavy showers',95:'⛈ Thunderstorm',99:'⛈ Heavy thunderstorm'}
cur = d.get('current', {})
daily = d.get('daily', {})
temp = cur.get('temperature_2m', '?')
wind = cur.get('wind_speed_10m', '?')
code = cur.get('weather_code', 0)
desc = wc.get(code, '?')
# Today
hi0 = daily.get('temperature_2m_max', [None])[0]
lo0 = daily.get('temperature_2m_min', [None])[0]
rain0 = daily.get('precipitation_sum', [None])[0]
# Tomorrow
hi1 = daily.get('temperature_2m_max', [None, None])[1]
lo1 = daily.get('temperature_2m_min', [None, None])[1]
rain1 = daily.get('precipitation_sum', [None, None])[1]
code1 = daily.get('weather_code', [0,0])[1]
desc1 = wc.get(code1, '?')
print(f'  Now: {desc} {temp}°C | Wind: {wind} km/h')
print(f'  Today: High {hi0}°C / Low {lo0}°C | Rain: {rain0}mm')
print(f'  Tomorrow: {desc1} High {hi1}°C / Low {lo1}°C | Rain: {rain1}mm')
" 2>/dev/null || echo "  (weather parse error)"
else
  echo "  (weather unavailable)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Uranium spot
echo "  ⚛️  U3O8 spot: ~$85.95/lb (SEQH confirmed Mar 9, 2026)"
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
