#!/bin/bash
# Reddit monitor — uses web_fetch equivalent via curl
# Monitors key subreddits for uranium/nuclear/war content

SUBS=("UraniumSqueeze" "wallstreetbets" "investing" "stocks" "energy" "nuclear")
SEARCHES=("uranium" "CCJ cameco" "NexGen uranium" "nuclear energy")

for sub in "${SUBS[@]}"; do
    echo "=== r/$sub (hot) ==="
    curl -s "https://www.reddit.com/r/$sub/search.json?q=uranium+OR+nuclear+OR+CCJ&sort=new&limit=5&t=day" \
         -H "User-Agent: OpenClaw-Monitor/1.0" 2>/dev/null | \
    python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    posts=d['data']['children']
    for p in posts[:3]:
        pd=p['data']
        print(f'• {pd[\"title\"][:100]}')
        print(f'  👍{pd[\"score\"]} 💬{pd[\"num_comments\"]} r/{pd[\"subreddit\"]}')
except: print('  (no results)')
" 2>/dev/null
    echo ""
done
