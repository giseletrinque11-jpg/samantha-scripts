#!/usr/bin/env python3
"""
Toiture Fortin — Customer Follow-Up Email Campaign
Reads clients.json, sends follow-up emails to clients not contacted in X days.
Usage: python3 followup_emails.py [--dry-run]
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timedelta

CLIENTS_FILE = os.path.expanduser("~/.openclaw/workspace/data/clients.json")
DRY_RUN = "--dry-run" in sys.argv

def send_email(to, name, dry_run=False):
    subject = "Toiture Fortin — Besoin d'entretien pour votre toiture?"
    first_name = name.split()[0]
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
        print(f"[DRY RUN] Would send to: {to}")
        print(f"Subject: {subject}")
        return True

    result = subprocess.run(
        ["gog", "gmail", "send",
         "--to", to,
         "--subject", subject,
         "--body", body],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Sent to {name} <{to}>")
        return True
    else:
        print(f"❌ Failed to send to {to}: {result.stderr}")
        return False


def main():
    with open(CLIENTS_FILE) as f:
        data = json.load(f)

    interval = data.get("followup_interval_days", 45)
    cutoff = datetime.now() - timedelta(days=interval)
    today = datetime.now().strftime("%Y-%m-%d")

    sent_count = 0
    for client in data["clients"]:
        last = client.get("last_contact", "2000-01-01")
        last_dt = datetime.strptime(last, "%Y-%m-%d")

        if last_dt <= cutoff:
            success = send_email(client["email"], client["name"], dry_run=DRY_RUN)
            if success and not DRY_RUN:
                client["last_contact"] = today
                sent_count += 1

    if not DRY_RUN and sent_count > 0:
        data["last_followup"] = today
        with open(CLIENTS_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nDone. {sent_count} follow-up email(s) sent. clients.json updated.")
    elif DRY_RUN:
        print(f"\n[DRY RUN complete — no emails sent]")
    else:
        print("No clients due for follow-up today.")


if __name__ == "__main__":
    main()
