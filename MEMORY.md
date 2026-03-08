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
