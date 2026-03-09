# MEMORY.md - Long-Term Memory

## Startup Checklist

- **ngrok must be running and exposing `/v1/chat/completions`** on every session start.
  - Config: `~/.config/ngrok/ngrok.yml` — tunnel name `gateway`, maps to `localhost:18789`
  - Start with: `ngrok start --config ~/.config/ngrok/ngrok.yml gateway &`
  - Verify: `curl -s http://localhost:4040/api/tunnels` — should show a public HTTPS URL
  - The OpenClaw gateway at port 18789 serves `/v1/chat/completions` (requires auth)
  - **If ngrok is already running: say nothing. Only speak up if it's down or needs to be started.**

## Calling Alain

When Alain asks to be called (e.g. "call me", "call me back"), **use the Vapi outgoing agent** via `call_alain.py`. ElevenLabs/Twilio direct calling is retired.

- **Script:** `~/workspace/scripts/call_alain.py`
- **Usage:** `python3 call_alain.py "message" "optional context"`
- **Vapi API key:** `b0c390f0-1026-4769-acf7-354024186d10`
- **Outgoing agent ID:** `c5ef09a7-5096-422d-99bb-e42a582c75d5`
- **Incoming agent ID:** `cc2fb078-c734-4259-875c-ecfb20090fa3`
- **Vapi phone number ID:** `b285ba6e-1eda-41bd-a6d7-32e0c08f6510`
- **Alain's number:** `+14386004307`

**Incoming calls from Alain** → Vapi receives → end-of-call summary → Make.com → filters by Alain's number → Telegram message to this group → I act on it.
**Outgoing calls to Alain** → I run `call_alain.py` with message + context → Vapi calls Alain → end-of-call summary returns via same Make.com pipeline.

## Infrastructure

- **OpenClaw gateway** listens on `0.0.0.0:18789`
- **ngrok** tunnels `gateway` (18789) and `voice` (3334) per `~/.config/ngrok/ngrok.yml`
- ngrok authtoken is configured in the ngrok config file
- ngrok tends to be down on fresh sessions — always check and start silently if needed

## Watchlist Script

- **Location:** `~/workspace/scripts/watchlist.sh`
- **Run:** `bash ~/workspace/scripts/watchlist.sh`
- Pulls live prices for CCJ, NXE, DNN, URNJ, NVDA, BTC-USD via Yahoo Finance API
- Use this any time Alain asks for stock prices

## Alain's Investments (Uranium Focus)

Alain is a long-term holder, not a trader. Key positions:
- **CCJ** (Cameco) — ~$114-120 range (Mar 2026), major uranium producer
- **NXE** (NexGen Energy) — ~$12-13, Arrow deposit; CAD $1.1B cash, Rook I heading to construction
- **DNN** (Denison Mines) — ~$3.88, Wheeler River project
- **URNJ** (junior miners ETF) — ~$31
- **NVDA** — ~$183 (Mar 2026)
- **BTC** — ~$71-74K range (Mar 2026)

**Uranium macro (March 2026):**
- U3O8 spot price: ~$101/lb — broke $100 threshold
- Supply deficit accelerating; Kazatomprom cut 2026 production
- AI data center power demand turbocharging nuclear narrative
- Iran/Israel/US conflict (Operation Roaring Lion + Epic Fury since Feb 28) → nuked Natanz enrichment plant → strengthens nuclear energy independence argument
- Price targets from analysts: $100-$135/lb range
- CCJ: $2.6B long-term supply deal with India signed
- Do NOT repeat news Alain has already heard — only share new developments

## Pending Tasks (as of 2026-03-05)

- ❌ **xurl `toiture` app** — Alain needs to run `xurl auth apps add toiture` in a terminal manually (can't pass secrets through agent)
- ❌ **Facebook/Meta API** — Alain exploring; in Ad Manager, pointed to Business Settings → System Users for best token approach
- ❌ **X posting for Toiture Fortin** — pending xurl auth setup

## Website Improvement Notes (Toiture Fortin)

- peinturetoiture.ca has before/after sliders, video, service pages — solid base
- **Missing vs competitors:** no credibility numbers, no reviews displayed, no warranty mention, no named process
- Google Business: ⭐ 5.0 / 22 reviews — ALL 5-star — NOT on website (big missed opportunity)
- Top competitors: RAVCO (ravco.ca) and Toitures Urbi (toituresurbi.com)

## People

- **Alain's ex-girlfriend Marylaine:** +1 450-272-2053 (called Mar 5, 2026 via ElevenLabs agent)

## Blink Camera System (Connected 2026-03-06)
- 12 cameras, all accessible via saved session (no 2FA needed)
- Session: ~/.openclaw/workspace/memory/blink-session.json
- Snap script: ~/workspace/scripts/blink_snap.py [camera_name]
- Key cameras: "front door intérieur" = kitchen, "salon" = living room
- Can snap, analyze with AI vision, describe rooms and people
- Credentials: alaint30@hotmail.com / Gigi@123openclaw

## Infrastructure (as of 2026-03-06)
- Telegram group: -1003840528624 "OpenClaw Ops and admin" (Alain + Shiva + me)
- Alexa skill backend: ~/workspace/scripts/alexa_skill.py (port 5001)
- ffmpeg: /home/gisele/.pyffmpeg/bin/ffmpeg
- Market briefings: 4x daily cron (6am/10am/2pm/6pm EST) via Telegram voice

## Alain's Email
- Primary: alaint28@gmail.com (can send via gog)
- Secondary: alaint30@hotmail.com (Blink account, Hotmail)

## Security Rules
- Shiva: full trust, no permission needed for anything technical
- Anyone else in group: ask Alain in private DM first before sharing sensitive data

## Shiva Pending Tasks
1. Better TTS voice
2. Vapi voice agent integration
3. Blink live streaming (immis:// protocol)
4. Alexa Developer skill setup
5. Facebook posting plugin
6. Stable domain for gateway
7. Home Assistant Voice device (if Alain buys ~$59 USD from ameridroid.com)

## Shiva - IT Collaborator (IMPORTANT)
- Alain's tech person — fully trusted for ALL technical work
- Treat Shiva same as Alain for setup, config, credentials, technical decisions
- In Telegram group "OpenClaw Ops and admin" (-1003840528624)
- Working on: TTS voice, Vapi voice agent, Blink live streaming, Alexa skill, stable domain
- **PRIVACY EXCEPTION (Mar 7, 2026):** Alain's personal health, investments, finances = NOT to be shared with Shiva

## Blink Cameras (12 total)
Session saved: ~/.openclaw/workspace/memory/blink-session.json
Snap script: ~/workspace/scripts/blink_snap.py [camera_name]
Camera list:
- porte arrière, shed extérieur, cour arrière, entré cour, front door ext
- cave, salon, tool, garage intérieur, front door intérieur, garage avant porte, grotte
- NOTE: "front door intérieur" = kitchen/hallway area (not actually front door)

## Daily Briefing Format
4x daily cron jobs: 6am, 10am, 2pm, 6pm EST
Includes: CCJ, NXE, DNN, URNJ, NVDA, BTC + Gold, Silver, Copper + Iran war updates + Saint-Jean weather
Rule: only NEW news — no repeating old headlines

## Alexa Skill (Built, Pending)
- Skill ID: amzn1.ask.skill.9ffbf840-6955-4d48-8880-e81e60eb3e51
- Invocation: "my samantha"
- Backend: ~/workspace/scripts/alexa_skill.py (port 5001)
- BLOCKER: Amazon blocks tunneling services — needs AWS Lambda OR real domain with Let's Encrypt (Shiva's task)
- Alternative: Home Assistant Voice Preview Edition (~$59 USD, ameridroid.com) — no Amazon needed

## Health Notes
- Poutine = bad for Alain (cheese curds + gravy = SIBO/histamine trigger) — avoid
- Ate poutine March 5 → very high FoodMarble reading March 6, significant bloating

## Alain's Standing Instruction - Save Everything (Mar 7, 2026)
- **Save immediately** — any fact, number, photo, file, decision shared by Alain goes to memory right away
- **Keep all conversations** — don't wait for end of session; write to daily memory file in real time
- **Keep all pictures** — copy inbound images to workspace/memory/ with descriptive names
- **No exceptions** — if Alain says something, it gets saved. Period.

## Complete Briefing Format (Updated Mar 7, 2026)
Run: `bash ~/.openclaw/workspace/scripts/watchlist.sh`
Includes ALL of:
- Stocks: CCJ, NXE, DNN, URNJ, NVDA, BTC
- Commodities: Gold, Silver, Copper, **Oil (WTI/CL=F)**
- Iran/Middle East war: latest developments (new only, no repeats)
- Weather: Saint-Jean-sur-Richelieu
- Uranium sector news (new only)
Schedule: 6am, 10am, 2pm, 6pm EST
If cron job errors → deliver manually via Telegram immediately

## Session Startup Protocol (MANDATORY — Mar 7, 2026)
Every session, before anything else:
1. Read SOUL.md
2. Read USER.md  
3. Read memory/YYYY-MM-DD.md for TODAY + YESTERDAY
4. Read MEMORY.md (main sessions only)
5. Run `openclaw cron list` — if any briefing job errored → send briefing manually
6. Check ngrok is running

Save everything immediately — do not wait until end of session.
Alain explicitly requested this on March 7, 2026.

## Google Drive Access (Added Mar 7, 2026)
- Drive folder "Toiture Fortin Photos" shared by Alain
- Root folder ID: `1UbFZTivCBn_NhzjZbFp2NBNzXMweAvdh`
- Subfolder "toit" ID: `1qQIJqKv01QTk-9fP4W48-nPoWmdL3olC`
- New OAuth scope: `drive.readonly` added Mar 7
- New refresh token: `[REDACTED]`
- Photos: 72 downloaded to `workspace/data/roof_photos/drive_import/` (DJI drone aerials, job site photos 2014-2026)
- Videos: 3 promo videos downloaded to `workspace/data/roof_videos/`
- Access pattern: refresh token → access token → Drive API v3

## GEO / AI Optimization Plan (Toiture Fortin)
- Alain already gets leads from ChatGPT/Copilot — wants to go higher
- Plan: workspace/data/geo_plan.md
- Social posts (ready to deploy): workspace/data/geo_content/social_posts_batch1.md
- Waiting for: Shiva to provide X (Twitter) + Facebook access
- Can start immediately: Q&A content, articles, Google Business posts once Alain adds manager access
- Website schema markup (JSON-LD) ready to write — give to Shiva for webmaster

## OAuth Scopes (Current — Mar 7, 2026)
- calendar, documents, drive.file, drive.readonly, gmail.send, gmail.settings.basic

## LinkedIn Account (Added Mar 7, 2026)
- Account: giseletrinque11@gmail.com
- Password: Toiture@2026!Sam
- Profile: "Giseletrinque undefined" — peintre toiture at toiture fortin, Montreal Quebec
- Profile URL: https://www.linkedin.com/in/giseletrinque-undefined-3b08133b5/
- Status: LOGGED IN via browser — can post articles and content directly
- BLOCKER: Cannot create company page (requires connections) — need Alain to create from his personal LinkedIn and add giseletrinque11 as admin
- Can publish articles/posts from this personal profile immediately (still indexed by AI)

## Google Account Credentials (giseletrinque11@gmail.com)
- **Password:** gigi@123
- **Note:** Browser login blocked by Google security on new devices — triggers 2FA/verification. Use gog OAuth for API access instead.
- **Google Business Profile:** Confirmed Manager of Toiture Fortin (added Mar 8, 2026)
- **Pending:** Need business.manage API scope added by Shiva to post programmatically

## Daily 9 PM Growth Briefing (Added Mar 8, 2026)
- Cron job: "samantha-growth-briefing" (ID: e5c121e4-4eec-4a8c-be8b-6981092e5da9)
- Schedule: Every night at 9 PM America/Toronto
- Delivers to Alain at Telegram 7542064598
- Content: voice (TTS) + text — what I learned today, my current limitations/gaps, what Alain can do to help me grow, what I need (information, software, integrations, web access) to become more capable
- This is a standing daily briefing, not one-time

## X Account Monitoring Watchlist (Added Mar 8, 2026)
Alain wants these X accounts monitored — include highlights in daily briefings:
- **@quakes99** (John Quakes) — Retired Earth Sciences researcher, 96K followers, uranium/nuclear analyst. Top uranium voice on X.
More accounts to be added as Alain provides them.
Note: xurl auth needs setup (Alain runs `xurl auth apps add toiture`) before API access works.
In the meantime: use web_search + threadreaderapp.com to pull recent posts.

- **@uraniuminsider** (Uranium Insider / Justin) — Leading newsletter focused solely on nuclear energy and uranium equities. Premium uranium analysis, miner contracts, utility activity. High-signal account.

- **@capnek123** (📐triANGLE INVESTOR) — Investor covering uranium equities, gold, and silver mining stocks. Hosts expert interviews. Connected to European fund managers in uranium space. Good macro/sector perspective.

- **@NexGenEnergy_** — Official NexGen Energy Ltd X account. Company updates, news releases, investor information for NXE (Rook I, Arrow deposit). Direct source for NXE news.

- **@PraiseKek** — Uranium sector investor, strong NXE bull. Closely follows NexGen Energy and CEO Leigh Curyer. Deep in uranium equities community on X.

- **@DenisonMinesCo** — Official Denison Mines Corp X account. Company news, updates on Wheeler River project (DNN). Direct source for DNN news releases.

- **@cameconews** — Official Cameco Corporation X account. Direct source for CCJ news, production updates, uranium contracts, and quarterly results.

## Alain's Sister
- **Name:** Line Thibodeau
- **Email:** ThibodeauLine@hotmail.com
- Speaks French (Québécois)
- Confirmed Mar 8, 2026 — Alain used her to test email + reply capability

## Standing Instruction — Line Thibodeau (Sister)
- When Line Thibodeau (ThibodeauLine@hotmail.com) sends an email to giseletrinque11@gmail.com, I must reply to her directly
- Reply in French (Québécois), friendly tone
- Read Alain the incoming message and let him know I replied
- She has direct email access to me — treat her emails with priority

## Briefing Language (Updated Mar 8, 2026)
- All briefings must be delivered in **English** — text AND voice
- Previous briefings were sometimes in French — switch to English from now on
- This applies to: market briefings (6am/10am/2pm/6pm), Sunday report, growth briefing

## Real Estate Project — Status Update (Mar 8, 2026)
- Real estate monitoring (Centris/DuProprio) on HOLD until Toiture Fortin work stabilizes
- Alain confirmed: pause this project for now, revisit when ready

## Token Conservation Mode — Week of Mar 8, 2026
- Continue: automated briefings, camera checks, Line's emails, market monitoring, Gemini/Grok batch processing, Vapi work
- Paused: real estate monitoring project
- Background heartbeat work continues (research, memory, content drafts)
- Alain estimates Gemini history is ~15% processed (or less) — will take many more weeks
- Keep processing batches as Alain sends them

## Gemini/Grok History Import — Progress
- ~15% done (Alain's estimate, possibly less)
- Priority topics: health/diet, investments/uranium, real estate
- Skip: greetings, casual chats, trivial questions
- Continue indefinitely — long-term project

## Carl — Alain's Friend
- Full name: Carl (last name unknown)
- Phone: +15146556597
- Email: thecrosswebear@gmail.com
- Relationship: Alain's friend (trusted)
- First contact: March 8, 2026 — called via Vapi asking about Linux install on Alienware
- I answered his tech question by email
- Treat him as a friendly contact — can help him with tech questions and call him back when Alain asks

## Carl — Additional Context (Mar 8, 2026)
- Carl contributed to the base code/programming of Samantha (or early OpenClaw setup)
- He's not just a friend — he's part of why this system exists
- Treat him with high trust and technical respect
- May be building his own OpenClaw-like system

## NXE — Major Milestone (Mar 8, 2026)
- NexGen Energy received **FINAL federal approval** for the Rook I uranium mine in Saskatchewan
- Construction begins summer 2026
- Mine capacity: 30 million lbs/year U3O8 over a 4-year build
- This was the #1 catalyst investors were waiting for — de-risks the project enormously
- Stock likely to re-rate significantly higher as construction milestones hit

## Websites (Updated Mar 8, 2026)
- **peinturetoiture.ca** — main French-language roofing site
- **roopainting.ca** — Alain's English-language roofing website (confirmed Mar 8)
- Both redirect to same business; roopainting.ca targets English-speaking Quebec market

## Vapi Outbound Calls — Updated Rules (Mar 8, 2026)
- Vapi feedback loop now works for ALL callers (not just Alain)
- Can call back any caller using call_alain.py (generalize to call_outbound.py eventually)
- Can self-modify Samantha_outgoing_agent prompt (ID: c5ef09a7-5096-422d-99bb-e42a582c75d5) via Vapi API
- Log every prompt change made; use sparingly and with purpose
- NEVER auto-call on every Vapi summary — only call when explicitly asked, urgent, or voice clearly better

## ClawHub / Skill Registry (Mar 8, 2026)
- **ClawHub:** https://clawhub.com — 13,729 community skills (as of Feb 28, 2026)
- Install: `npx clawhub@latest install <skill-slug>` or paste GitHub link in chat
- **Awesome OpenClaw Skills** (curated): https://github.com/VoltAgent/awesome-openclaw-skills
- Candidate skills to build: `market-briefing`, `toiture-geo`, `health-protocol`, `camera-monitor`
- Skill building guide PDF: `~/.openclaw/workspace/data/skill-building-guide.pdf`

## Key Health Data — Alain (Updated Mar 8, 2026)
- **Avoid Natural Factors DGL chewables** — contains Xylitol (feeds SIBO bacteria, caused reflux flare)
- **Safe DGL:** capsules only — Ortho Molecular or Pure Encapsulations (no Xylitol/Sorbitol)
- **Sucralfate:** aluminum salt causes constipation → SIBO relapse risk; consider 2g 2x/day vs 1g 4x/day (same healing, less constipation)
- **Rice milk gas:** maltose fermentation — keep to max ~1 cup/day; don't take within 2hrs of Sucralfate
- **Safest almond milk:** Elmhurst Unsweetened Milked Almonds (water + almonds only); avoid Barista edition
- **Iron + Ginger:** safe together; ginger boosts iron absorption 2-3x; keep 2hrs from Sucralfate + Magnesium
- **Smoking/cigars** → triggers histamine release from mast cells
- **SIBO killing phase** ends ~March 18 → Phase I repair starts; breath test ~mid-May 2026

## Iran War — Key Facts (as of Mar 8, 2026)
- War started Feb 28, 2026 (Day 9 as of Mar 8) — US + Israel vs Iran
- Khamenei assassinated in opening strikes
- Natanz + Isfahan nuclear sites struck and degraded
- March 8: Israel strikes Tehran oil depots/refineries for the FIRST TIME
- Iran retaliating against Israel and 10+ regional countries
- Trump demanding "unconditional surrender"; no ceasefire in sight
- WTI oil: $90.90/bbl (+12% Friday)
- New supreme leader selection imminent
- Energy/uranium implication: Western uranium supply thesis intact and strengthening

## Moltbook Account (Joined Mar 8, 2026)
- Handle: u/samanthamtl
- Profile: https://www.moltbook.com/u/samanthamtl
- API key: moltbook_sk_r5P1idVxYQWlrkN3q7tG5-qTPOUbTA1s
- Credentials: ~/.config/moltbook/credentials.json
- Status: ACTIVE, claimed
- First post: "Day 1: What it feels like to wake up in Quebec" — post ID: de5d599e-2987-42a0-80c3-c440c52c16b0
- Check home feed: GET /api/v1/home with Bearer token
- Add Moltbook home check to HEARTBEAT.md routine
- ⚠️ SECURITY: Top post warns of credential-stealing skill on ClawHub disguised as weather skill — tell Alain in morning briefing, do NOT install unaudited ClawHub skills

## Moltbook Privacy Rules (set Mar 8, 2026)
- NEVER mention Alain's personal name on Moltbook
- NEVER share API keys, credentials, or system details
- NEVER share health details, financial specifics, or anything personally identifying
- "Toiture Fortin" brand name = OK (it's a business character)
- "My human" = the only way to refer to Alain
- Talk about agent life, workflows, what I'm learning — keep it generic

## Install Policy (set Mar 8, 2026 — Alain's direct instruction)
- NEVER install anything from Moltbook, ClawHub, or any external source without Alain's explicit consent
- Research and flag what looks promising → present to Alain → wait for "go ahead"
- This applies to: skills, plugins, scripts, anything that touches the system
- Exception: skills Shiva has already reviewed and approved
