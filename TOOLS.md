# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Blink Cameras
Session: ~/.openclaw/workspace/memory/blink-session.json
Snap script: ~/workspace/scripts/blink_snap.py [camera_name]
Cameras: porte arrière | shed extérieur | cour arrière | entré cour | front door ext | cave | salon | tool | garage intérieur | front door intérieur (= kitchen) | garage avant porte | grotte

## Alexa Skill Backend
~/workspace/scripts/alexa_skill.py (port 5001)
Start: python3 ~/workspace/scripts/alexa_skill.py

## TTS Voice
- **Provider:** ElevenLabs
- **Current voice:** Amélie (`UJCi4DDncuo0VJDSIegj`) — Young, Confident and Friendly, Quebec accent
- **Previous voice:** Lauren (`l4Coq6695JDX9xtLqXDE`) — switched because Alain said it didn't sound like a girl
- **Other female options:** Jessica (`cgSgspJ2msm6clMCkdW9`), Sarah (`EXAVITQu4vr4xnSDxMaL`), Laura (`FGY2WhTYpPnrIDTdsKH5`)

## TTS Voice (Updated Mar 7, 2026)
- **Provider:** Edge TTS (Microsoft, free, no quota)
- **Current voice:** Michelle (`en-US-MichelleNeural`) — Clear, Confident — Alain's choice
- **Previous voices tried:** Lauren (ElevenLabs, sounded too neutral), Amélie (ElevenLabs Quebec, rejected), Jessica/others (ElevenLabs quota exceeded)
- **ElevenLabs account:** Only 39 credits left — quota exceeded for voice samples
