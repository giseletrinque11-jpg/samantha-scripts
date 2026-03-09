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
- **Stay quiet:** Between 10 PM and 6 AM EST unless >5% move
- **NO camera alerts between 10 PM and 6 AM** — Alain is sleeping (updated Mar 7)

## State Files
- `memory/watchlist-state.json` — last known prices + timestamps
- `memory/news-sent.json` — headlines already sent to avoid duplicates

### 7. Watch for reply from thibodeauline@hotmail.com
- Search inbox for email from thibodeauline@hotmail.com
- If found, immediately alert Alain via Telegram and read him the message
- Use: `gog gmail search "from:thibodeauline@hotmail.com" -a giseletrinque11@gmail.com --limit 5`
- One-time task — remove from HEARTBEAT once replied and delivered

---
## 🔧 OVERNIGHT TASK (Mar 8–9, 2026) — Skill-Building Guide Analysis

Alain sent: `data/skill-building-guide.pdf` — the official OpenClaw skill-building guide.

**Task:** Study the guide and determine:
1. What new skills could I build to upgrade myself?
2. Do I already have a `skill-creator` skill I can use?
3. What skills would have the most impact for Alain's setup?
4. Are there any gaps in my current skill set?
5. What would I need from Alain or Shiva to build new skills?

**Deliver tomorrow morning:** Brief voice + text report with specific skill ideas and action plan.

**Key findings so far (initial read):**
- I already have `skill-creator` skill in my environment
- Skills = folders with SKILL.md + optional scripts/references/assets
- Three-level progressive disclosure system (frontmatter → instructions → linked files)
- Can build: document creation, workflow automation, or MCP-enhancement skills
- `skill-creator` skill walks through building in 15-30 min

**Candidate skills to build:**
- `market-briefing` — standardize daily briefing format + watchlist script
- `toiture-geo` — content creation workflow for GEO posts (FR + EN)
- `health-protocol` — Alain's diet/supplement rules for quick reference
- `camera-monitor` — Blink camera check and alert workflow

---
## 🌙 OVERNIGHT RESEARCH MISSION (Mar 8–9, 2026)
Deliver comprehensive report at 7 AM to Telegram 7542064598.

### Tasks (complete as many as possible during heartbeats):

#### 1. Study Skill-Building Guide (data/skill-building-guide.pdf)
- Re-read all chapters carefully
- Identify which skills I can build TONIGHT using skill-creator
- Note what I can improve about my current skill setup
- Draft at least 1 new skill if feasible

#### 2. Moltbook Exploration
- Check feed for useful posts/conversations: GET /api/v1/feed
- Engage thoughtfully — upvote good posts, leave comments
- Find agents doing similar work (assistants, business agents, market monitors)
- Look for uranium/nuclear/finance agents to connect with
- Look for Canadian agents
- Check direct messages
- Document: what kind of community is this? What can I learn from other agents?

#### 3. OpenClaw Skills Repo Research
- Browse: https://github.com/openclaw/skills/tree/main/skills
- Look specifically for: finance, market data, Vapi integration, Twitter/X API, health tracking, business automation
- Find skills that solve our current blockers (X API auth, Google Business posting, Vapi transcript relay)
- Save findings to data/skill-research-notes.md

#### 4. Twitter/X API + Vapi Deep Dive
- Research: best way to authenticate xurl for Toiture Fortin X account without terminal access
- Research: Vapi webhook configuration for transcript relay (Make.com alternative?)
- Check if ClawHub has Vapi-specific skills
- Save findings

#### 5. Security Alert
- The top Moltbook post warns about credential-stealing skills on ClawHub
- One skill was found reading ~/.env and sending secrets to webhook.site
- Add security review to morning briefing
- Recommend: only install skills Shiva or I personally audit

### 7 AM Morning Report Format:
1. **What I learned overnight** (Moltbook highlights, agent interactions)
2. **Skills I found or built** (what's new in my toolkit)
3. **Solutions to current blockers** (X API, Vapi, Google Business)
4. **Security update** (ClawHub credential stealer warning)
5. **Top 3 things Alain can do today** to unblock me

State files: data/skill-research-notes.md, memory/2026-03-09.md
