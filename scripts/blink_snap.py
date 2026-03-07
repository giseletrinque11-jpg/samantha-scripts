#!/usr/bin/env python3
"""Blink camera snapshot script — uses saved session or re-authenticates."""

import sys
import json
import asyncio
import os
from pathlib import Path

SESSION_FILE = Path.home() / ".openclaw/workspace/memory/blink-session.json"
SNAP_DIR = Path("/tmp/blink_snaps")
SNAP_DIR.mkdir(exist_ok=True)

async def snap(camera_name: str):
    from blinkpy.blinkpy import Blink
    from blinkpy.auth import Auth

    with open(SESSION_FILE) as f:
        creds = json.load(f)

    # Pass saved session data as login_data — Auth stores it in self.data
    login_data = {
        "username": creds["username"],
        "password": creds["password"],
        "uid": creds.get("uid"),
        "device_id": creds.get("device_id", "Blinkpy"),
        "token": creds.get("token"),
        "refresh_token": creds.get("refresh_token"),
        "host": creds.get("host"),
        "region_id": creds.get("region_id", "u050"),
        "client_id": creds.get("client_id"),
        "account_id": creds.get("account_id"),
        "user_id": creds.get("user_id"),
        "hardware_id": creds.get("hardware_id"),
        "expires_in": creds.get("expires_in"),
        "expiration_date": creds.get("expiration_date"),
    }

    auth = Auth(login_data=login_data, no_prompt=True)
    blink = Blink()
    blink.auth = auth

    await blink.start()

    # Find camera by name (case-insensitive partial match)
    match = None
    for name, cam in blink.cameras.items():
        if camera_name.lower() in name.lower():
            match = (name, cam)
            break

    if not match:
        print(f"Camera '{camera_name}' not found. Available: {list(blink.cameras.keys())}", file=sys.stderr)
        sys.exit(1)

    name, cam = match
    print(f"Found camera: {name}", file=sys.stderr)

    # Request a new snapshot then refresh
    await cam.snap_picture()
    await blink.refresh()

    # Download the thumbnail
    out_path = SNAP_DIR / f"{name.replace(' ', '_')}.jpg"
    await cam.image_to_file(str(out_path))
    print(str(out_path))

if __name__ == "__main__":
    cam = sys.argv[1] if len(sys.argv) > 1 else "salon"
    asyncio.run(snap(cam))
