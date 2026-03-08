#!/usr/bin/env python3
"""Simple Alexa skill backend for Samantha."""
import requests, json, logging, os
from pathlib import Path
from flask import Flask, request, jsonify

# Load .env from workspace root
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

OPENCLAW_URL = "http://localhost:18789/v1/chat/completions"
OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN")

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

def ask_samantha(query):
    try:
        resp = requests.post(
            OPENCLAW_URL,
            headers={"Authorization": f"Bearer {OPENCLAW_TOKEN}", "Content-Type": "application/json"},
            json={
                "model": "anthropic/claude-sonnet-4-6",
                "messages": [
                    {"role": "system", "content": "You are Samantha, Alain's AI assistant. Keep responses short and natural for spoken audio — 2-3 sentences max, no markdown."},
                    {"role": "user", "content": query}
                ],
                "max_tokens": 200
            },
            timeout=15
        )
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, I'm having trouble right now. Try again."

def alexa_response(speech, should_end=False, reprompt=None):
    r = {"version": "1.0", "response": {"outputSpeech": {"type": "PlainText", "text": speech}, "shouldEndSession": should_end}}
    if reprompt:
        r["response"]["reprompt"] = {"outputSpeech": {"type": "PlainText", "text": reprompt}}
    return jsonify(r)

@app.route("/alexa", methods=["POST"])
def alexa():
    body = request.json
    req_type = body.get("request", {}).get("type", "")
    
    if req_type == "LaunchRequest":
        return alexa_response("Hey Alain! Samantha here. What do you need?", reprompt="What can I help you with?")
    
    elif req_type == "IntentRequest":
        intent = body["request"]["intent"]["name"]
        
        if intent == "SamanthaIntent":
            slots = body["request"]["intent"].get("slots", {})
            query = slots.get("query", {}).get("value", "")
            if query:
                answer = ask_samantha(query)
                return alexa_response(answer, reprompt="Anything else?")
            return alexa_response("I didn't catch that. What would you like to know?", reprompt="What can I help with?")
        
        elif intent in ("AMAZON.StopIntent", "AMAZON.CancelIntent"):
            return alexa_response("Okay, talk soon!", should_end=True)
        
        elif intent == "AMAZON.HelpIntent":
            return alexa_response("Ask me anything. For example: ask Samantha, what's the CCJ price?", reprompt="What would you like to know?")
    
    elif req_type == "SessionEndedRequest":
        return jsonify({"version": "1.0", "response": {}})
    
    return alexa_response("Something went wrong. Try again.", should_end=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
