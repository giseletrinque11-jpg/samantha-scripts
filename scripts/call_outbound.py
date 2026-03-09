#!/usr/bin/env python3
"""
Trigger an outbound Vapi call to any number.
Usage: python3 call_outbound.py <phone_number> <name> "<message>" 

Examples:
  python3 call_outbound.py +15142162436 Alain "Bonjour, c'est Samantha. Rappel pour ton rendez-vous."
  python3 call_outbound.py +15146556597 Carl "Hi Carl, this is Samantha. I'm calling to clarify your request."
"""
import requests, sys, os
from pathlib import Path

# Load .env from workspace root
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

VAPI_KEY      = os.getenv("VAPI_KEY")
OUTGOING_ID   = os.getenv("VAPI_OUTGOING_AGENT_ID")
PHONE_NUM_ID  = os.getenv("VAPI_PHONE_NUMBER_ID")

def call_outbound(number: str, name: str, message: str):
    if not number.startswith("+"):
        print("Error: phone number must include country code, e.g. +15142162436")
        return None

    payload = {
        "assistantId": OUTGOING_ID,
        "phoneNumberId": PHONE_NUM_ID,
        "customer": {
            "number": number,
            "name": name
        },
        "assistantOverrides": {
            "firstMessage": message
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
        print(f"Call initiated to {name} ({number}). ID: {call_id}")
        return call_id
    else:
        print(f"Error {resp.status_code}: {resp.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 call_outbound.py <phone_number> <name> \"<message>\"")
        print("Example: python3 call_outbound.py +15142162436 Alain \"Bonjour, c'est Samantha.\"")
        sys.exit(1)

    number  = sys.argv[1]
    name    = sys.argv[2]
    message = sys.argv[3]

    call_outbound(number, name, message)
