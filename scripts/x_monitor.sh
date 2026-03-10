#!/bin/bash
# X/Twitter monitor: home feed + search + watchlist accounts
AUTH=""  # DISABLED - was using session cookies, flagged by X

echo "=== HOME FEED (latest) ==="
bird $AUTH home --plain 2>/dev/null | head -60

echo ""
echo "=== URANIUM/NUCLEAR SEARCH ==="
bird $AUTH search "uranium OR nuclear energy OR CCJ OR NexGen OR Rook1" --plain 2>/dev/null | head -60

echo ""
echo "=== IRAN WAR SEARCH ==="
bird $AUTH search "Iran war OR Iran nuclear OR Hormuz OR oil Iran" --plain 2>/dev/null | head -60

echo ""
echo "=== WATCHLIST ACCOUNTS ==="
for account in "quakes99" "uraniuminsider" "capnek123" "NexGenEnergy_" "PraiseKek" "DenisonMinesCo" "cameconews"; do
    echo "--- @$account ---"
    bird $AUTH user-tweets "$account" --plain 2>/dev/null | head -20
done

# ===== TOITURE FORTIN ACCOUNT =====
echo ""
echo "🏠 TOITURE FORTIN (@Toiture_Fortin)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ACCOUNT_RESULT=$(curl -s "https://api.twitter.com/2/users/by/username/Toiture_Fortin?user.fields=public_metrics" \
  -H "Authorization: Bearer ${CT0}" \
  -H "User-Agent: Mozilla/5.0" 2>/dev/null)
echo "Account status: monitoring (direct API auth needed for full data)"

# Search for competitor activity
echo ""
echo "🏠 COMPETITOR SCAN — Quebec roofing on X"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
COMPETITORS=$(curl -s "https://api.twitter.com/2/tweets/search/recent?query=toiture+quebec+-is:retweet&max_results=10&tweet.fields=created_at,author_id,text" \
  -H "Cookie: auth_token=${AUTH_TOKEN}; ct0=${CT0}" \
  -H "X-Csrf-Token: ${CT0}" \
  -H "User-Agent: Mozilla/5.0" 2>/dev/null)
echo "$COMPETITORS" | python3 -c "
import json,sys
try:
  d=json.load(sys.stdin)
  tweets=d.get('data',[])
  for t in tweets[:5]:
    print(f'  - {t[\"text\"][:100]}')
except: print('  (no data)')
" 2>/dev/null
