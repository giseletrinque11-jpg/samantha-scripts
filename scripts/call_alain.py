#!/usr/bin/env python3
"""
Trigger an outbound Vapi call to Alain.
Usage: python3 call_alain.py "Your message here" "Optional context"
"""
import requests, sys, json

VAPI_KEY      = "b0c390f0-1026-4769-acf7-354024186d10"
OUTGOING_ID   = "c5ef09a7-5096-422d-99bb-e42a582c75d5"
PHONE_NUM_ID  = "b285ba6e-1eda-41bd-a6d7-32e0c08f6510"
ALAIN_NUMBER  = "+14386004307"

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
