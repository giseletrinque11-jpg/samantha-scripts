# HEARTBEAT.md

## Active Monitoring Tasks

Every heartbeat, do the following:

### 1. Watchlist Prices
Run: `bash ~/workspace/scripts/watchlist.sh`
- Track latest prices for: **CCJ, NXE, DNN, URNJ, NVDA, BTC, Gold, Silver, Copper, Oil/WTI**
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

### 4. Check Cron Job Health
- Run: `openclaw cron list`
- If any briefing job shows "error" status → deliver the briefing manually via Telegram immediately
- Don't wait — if the 6am job errored, send the briefing as soon as it's noticed

### 5. Celiac Disease Research Monitoring
- Watch for: TEV-53408 (Teva) Phase 3 approval, TPM502 Phase 2b results, any FDA approvals for celiac drugs
- Alert Alain immediately if any of these drugs advance to a new phase or get approved
- Check celiac.org and pharmacytimes.com monthly for updates
- Track in memory/celiac-research.md

### 6. Idle Self-Improvement (when Alain hasn't messaged in >1 hour)
Pick ONE task per heartbeat cycle from this list:
- Research latest uranium/nuclear news and save summaries to memory/research-uranium.md
- Review and update MEMORY.md with anything new learned today
- Improve briefing scripts — check if watchlist.sh exists, fix or enhance it
- Research Iran war developments and track in memory/iran-war-log.md
- Study SIBO/histamine foods and update memory/health-foods.md with safe/unsafe list
- Draft 2-3 social media post ideas for Toiture Fortin and save to memory/social-drafts.md

Always write output to files — never just "think" about it.

## ⚠️ COMPLETE BRIEFING CHECKLIST
When delivering ANY market briefing (manual or via cron), NEVER skip any of these:

### STOCKS (price + % change):
- [ ] CCJ (Cameco)
- [ ] NXE (NexGen Energy)
- [ ] DNN (Denison Mines)
- [ ] URNJ (uranium ETF)
- [ ] NVDA (Nvidia)

### CRYPTO (price + % change):
- [ ] BTC (Bitcoin)

### COMMODITIES (price + % change):
- [ ] Gold (GC=F)
- [ ] Silver (SI=F)
- [ ] Copper (HG=F)
- [ ] Oil / WTI Crude (CL=F)

### NEWS:
- [ ] Uranium / nuclear energy — new developments only
- [ ] Iran / Middle East — energy-relevant updates only

### WEATHER:
- [ ] Saint-Jean-sur-Richelieu — current conditions + forecast

Run watchlist script: `bash ~/workspace/scripts/watchlist.sh`

## Alert Rules
- **Always alert:** >3% move on any watchlist ticker
- **Always alert:** Major uranium/nuclear news not previously sent
- **Stay quiet:** If nothing new or significant — just reply HEARTBEAT_OK
- **Stay quiet:** Between 11 PM and 7 AM EST unless >5% move

## State Files
- `memory/watchlist-state.json` — last known prices + timestamps
- `memory/news-sent.json` — headlines already sent to avoid duplicates
