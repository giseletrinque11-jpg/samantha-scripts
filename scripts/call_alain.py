#!/usr/bin/env python3
"""
Trigger an outbound Vapi call to Alain.
Usage: python3 call_alain.py "Your message here" "Optional context"
"""
import requests, sys, json, os
from pathlib import Path

# Load .env from workspace root
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

VAPI_KEY      = os.getenv("VAPI_KEY")
OUTGOING_ID   = os.getenv("VAPI_OUTGOING_AGENT_ID")
PHONE_NUM_ID  = os.getenv("VAPI_PHONE_NUMBER_ID")
ALAIN_NUMBER  = os.getenv("ALAIN_NUMBER")

def call_alain(message: str, context: str = ""):
    payload = {
        "assistantId": OUTGOING_ID,
        "phoneNumberId": PHONE_NUM_ID,
        "customer": {
            "number": ALAIN_NUMBER,
            "name": "Alain"
        },
        "assistantOverrides": {
            "firstMessage": f"Bonjour Alain, c'est Samantha. {message}",
            "model": {
                "messages": [
                    {
                        "role": "system",
                        "content": f"CONTEXT FOR THIS CALL: {context}" if context else "Deliver the firstMessage clearly and handle Alain's response."
                    }
                ]
            }
        }
    }

    resp = requests.post(
        "https://api.vapi.ai/call",
        headers={
            "Authorization": f"Bearer {VAPI_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=15
    )

    if resp.status_code == 201:
        call_id = resp.json().get("id", "unknown")
        print(f"Call initiated. ID: {call_id}")
        return call_id
    else:
        print(f"Error {resp.status_code}: {resp.text}")
        return None

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "J'ai une mise à jour pour toi."
    ctx = sys.argv[2] if len(sys.argv) > 2 else ""
    call_alain(msg, ctx)
