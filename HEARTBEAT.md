# HEARTBEAT.md

## Active Monitoring Tasks

Every heartbeat, do the following:

### 1. Watchlist Prices
Run: `bash ~/workspace/scripts/watchlist.sh`
- Track latest prices for CCJ, NXE, DNN, URNJ, NVDA, BTC
- Compare to last known prices (stored in memory/watchlist-state.json)
- If any ticker moves >3% since last check → send Alain a Telegram alert
- Update memory/watchlist-state.json with latest prices after each check

### 2. Uranium & Nuclear News
Search for: "uranium news", "CCJ", "NXE", "nuclear energy", "SMR"
- Only alert if genuinely NEW and significant (not repeat of already-sent news)
- Track sent headlines in memory/news-sent.json to avoid duplicates
- Worth alerting: price moves, new contracts, regulatory approvals, geopolitical events affecting supply

### 3. Market Context
- Check if Iran/US/Israel conflict has any new developments affecting energy/uranium
- Check for any SMR sector news (new contracts, regulatory milestones)

## Alert Rules
- **Always alert:** >3% move on any watchlist ticker
- **Always alert:** Major uranium/nuclear news not previously sent
- **Stay quiet:** If nothing new or significant — just reply HEARTBEAT_OK
- **Stay quiet:** Between 11 PM and 7 AM EST unless >5% move

## State Files
- `memory/watchlist-state.json` — last known prices + timestamps
- `memory/news-sent.json` — headlines already sent to avoid duplicates
