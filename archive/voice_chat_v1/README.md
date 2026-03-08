# voice_chat v1 — ARCHIVED 2026-03-07

## What it was
Flask-based web voice interface for Samantha.
- Browser mic (Web Speech API) → text → OpenClaw gateway → Claude → ElevenLabs TTS → audio playback
- Port: 5002
- Chrome only (Web Speech API requirement)

## Why archived
Being replaced by Vapi integration (Shiva's work).

## Known issues at time of archival
- ElevenLabs key hardcoded in plaintext (security risk)
- ElevenLabs key expired/quota exceeded — fell back to browser TTS
- Bound to 0.0.0.0 (should have been 127.0.0.1)
- No conversation memory (stateless)
- Single shared /tmp audio file (race condition risk)

## Status at archival
- Process killed (PID 3170459)
- Cloudflare tunnel killed (PID 3171814)
