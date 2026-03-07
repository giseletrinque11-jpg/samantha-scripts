#!/usr/bin/env python3
"""
Toiture Fortin — Customer Follow-Up Email Campaign
Mode 1 (default): notify Alain via Telegram for approval
Mode 2 (--send): actually send the emails (after Alain approves)
Usage: python3 followup_emails.py [--send] [--dry-run]
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timedelta

CLIENTS_FILE = os.path.expanduser("~/.openclaw/workspace/data/clients.json")
DRY_RUN = "--dry-run" in sys.argv
SEND_MODE = "--send" in sys.argv
ALAIN_TELEGRAM = "7542064598"

def telegram_notify(message):
    subprocess.run(
        ["openclaw", "message", "send", "--target", ALAIN_TELEGRAM,
         "--channel", "telegram", "--message", message],
        capture_output=True
    )

def send_followup_email(to, name, dry_run=False):
    first_name = name.split()[0]
    subject = "Toiture Fortin — Besoin d'entretien pour votre toiture?"
    body = f"""Bonjour {first_name},

Nous espérons que vous allez bien!

Nous voulions simplement vous rappeler que Toiture Fortin offre des services d'entretien et de peinture de toiture métallique dans votre région.

Si vous avez besoin d'une inspection, d'un rafraîchissement de votre revêtement élastomère, ou simplement d'un devis, nous serions heureux de vous aider.

N'hésitez pas à nous contacter :
📞 514 216-2436
🌐 toiturefortin.com

Cordialement,
Toiture Fortin"""

    if dry_run:
        print(f"[DRY RUN] Would send to: {name} <{to}>")
        return True

    result = subprocess.run(
        ["gog", "gmail", "send", "--to", to, "--subject", subject, "--body", body],
        capture_output=True, text=True
    )
    success = result.returncode == 0
    print(f"{'✅' if success else '❌'} {'Sent' if success else 'Failed'}: {name} <{to}>")
    return success

def main():
    with open(CLIENTS_FILE) as f:
        data = json.load(f)

    interval = data.get("followup_interval_days", 45)
    cutoff = datetime.now() - timedelta(days=interval)
    today = datetime.now().strftime("%Y-%m-%d")

    due = [c for c in data["clients"]
           if datetime.strptime(c.get("last_contact", "2000-01-01"), "%Y-%m-%d") <= cutoff]

    if not due:
        print("No clients due for follow-up.")
        return

    if not SEND_MODE:
        # APPROVAL MODE — ask Alain first
        names = ", ".join(c["name"] for c in due)
        msg = (f"📬 Monthly follow-up due for {len(due)} customer(s): {names}. "
               f"Reply 'yes send followup' to send the emails, or ignore to skip.")
        print(msg)
        # In cron context, this message goes to Alain via Telegram
        return

    # SEND MODE — actually send
    sent = 0
    for client in due:
        success = send_followup_email(client["email"], client["name"], dry_run=DRY_RUN)
        if success and not DRY_RUN:
            client["last_contact"] = today
            sent += 1

    if not DRY_RUN and sent > 0:
        data["last_followup"] = today
        with open(CLIENTS_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Done. {sent} follow-up email(s) sent.")

if __name__ == "__main__":
    main()
