# MEMORY.md - Long-Term Memory

## Startup Checklist

- **ngrok must be running and exposing `/v1/chat/completions`** on every session start.
  - Config: `~/.config/ngrok/ngrok.yml` — tunnel name `gateway`, maps to `localhost:18789`
  - Start with: `ngrok start --config ~/.config/ngrok/ngrok.yml gateway &`
  - Verify: `curl -s http://localhost:4040/api/tunnels` — should show a public HTTPS URL
  - The OpenClaw gateway at port 18789 serves `/v1/chat/completions` (requires auth)
  - **If ngrok is already running: say nothing. Only speak up if it's down or needs to be started.**

## Calling Alain

When Alain asks to be called (e.g. "call me", "call me back"), **always use the ElevenLabs agent**, not the built-in voice-call plugin.

- **Agent ID:** `agent_6401kjtb35rcfgrbbegf7cwc5cbx`
- **Phone number ID:** `phnum_3001kjrayzd4fkgb76t0gcmbgzbk`
- **API key env var:** `ELEVENLABS_API_KEY` (sk_5e84355...)
- **Alain's number:** `+14386004307`
- **Command:**
  ```bash
  curl -X POST "https://api.elevenlabs.io/v1/convai/twilio/outbound-call" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
    -d '{"agent_id": "agent_6401kjtb35rcfgrbbegf7cwc5cbx", "agent_phone_number_id": "phnum_3001kjrayzd4fkgb76t0gcmbgzbk", "to_number": "+14386004307"}'
  ```
- The ElevenLabs agent calls via Twilio and uses OpenClaw's `/v1/chat/completions` as its LLM — **ngrok gateway tunnel must be running** for the call to work.

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

- **Alain's friend Marilyn:** +1 450-272-2053 (called Mar 5, 2026 via ElevenLabs agent)
