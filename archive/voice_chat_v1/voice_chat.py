#!/usr/bin/env python3
"""Voice chat web interface for Samantha."""
import requests, json, logging, os
from flask import Flask, request, jsonify, Response

OPENCLAW_URL = "http://localhost:18789/v1/chat/completions"
OPENCLAW_TOKEN = "sk_c37dcbb0efc2251ebf1de3724e11772d4ab302ed5f520259"
ELEVENLABS_KEY = "sk_a8452c4814e1513982e515ed33548459c8aadc799c3dcdbf"
VOICE_ID = "l4Coq6695JDX9xtLqXDE"

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Samantha 🐙</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { 
    background: #0f0f1a; color: #e0e0e0; 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex; flex-direction: column; align-items: center; 
    justify-content: center; min-height: 100vh; padding: 20px;
  }
  h1 { font-size: 2em; margin-bottom: 8px; color: #a78bfa; }
  .subtitle { color: #6b7280; margin-bottom: 40px; font-size: 0.9em; }
  #status { 
    font-size: 1.1em; color: #a78bfa; margin-bottom: 30px; 
    min-height: 1.5em; text-align: center;
  }
  #micBtn {
    width: 120px; height: 120px; border-radius: 50%; 
    border: 3px solid #a78bfa; background: transparent;
    cursor: pointer; font-size: 3em; transition: all 0.3s;
    display: flex; align-items: center; justify-content: center;
  }
  #micBtn:hover { background: rgba(167,139,250,0.1); transform: scale(1.05); }
  #micBtn.listening { 
    background: rgba(239,68,68,0.2); border-color: #ef4444;
    animation: pulse 1s infinite;
  }
  #micBtn.thinking { 
    background: rgba(251,191,36,0.15); border-color: #fbbf24;
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
  }
  #transcript {
    margin-top: 30px; padding: 15px 20px; background: #1a1a2e;
    border-radius: 12px; max-width: 600px; width: 100%;
    min-height: 60px; color: #d1d5db; font-size: 0.95em;
    line-height: 1.6; display: none;
  }
  #response {
    margin-top: 15px; padding: 15px 20px; background: #1e1b4b;
    border-radius: 12px; max-width: 600px; width: 100%;
    min-height: 60px; color: #c4b5fd; font-size: 0.95em;
    line-height: 1.6; display: none;
  }
  .hint { margin-top: 20px; color: #4b5563; font-size: 0.8em; text-align: center; }
</style>
</head>
<body>
<h1>🐙 Samantha</h1>
<p class="subtitle">Your personal AI assistant</p>
<div id="status">Click the mic and speak</div>
<button id="micBtn" onclick="toggleListen()">🎙️</button>
<div id="transcript"></div>
<div id="response"></div>
<p class="hint">Works best in Chrome. Click mic, speak, release to send.</p>

<script>
let recognition = null;
let isListening = false;
let currentAudio = null;

const btn = document.getElementById('micBtn');
const status = document.getElementById('status');
const transcriptEl = document.getElementById('transcript');
const responseEl = document.getElementById('response');

function setStatus(msg, cls='') {
  status.textContent = msg;
  btn.className = cls;
}

function initRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setStatus('⚠️ Speech recognition not supported. Use Chrome.');
    return null;
  }
  const r = new SpeechRecognition();
  r.lang = 'en-US';
  r.continuous = false;
  r.interimResults = true;
  
  r.onresult = (e) => {
    let interim = '', final = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) final += e.results[i][0].transcript;
      else interim += e.results[i][0].transcript;
    }
    transcriptEl.style.display = 'block';
    transcriptEl.textContent = '🗣️ ' + (final || interim);
    if (final) sendToSamantha(final);
  };
  
  r.onerror = (e) => {
    setStatus('Error: ' + e.error + '. Click to try again.');
    isListening = false;
    btn.className = '';
  };
  
  r.onend = () => {
    isListening = false;
    if (btn.className === 'listening') {
      setStatus('Processing...');
      btn.className = 'thinking';
    }
  };
  
  return r;
}

async function sendToSamantha(text) {
  setStatus('🤔 Thinking...', 'thinking');
  responseEl.style.display = 'none';
  
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await res.json();
    const reply = data.reply || 'Sorry, I had trouble with that.';
    
    responseEl.style.display = 'block';
    responseEl.textContent = '🐙 ' + reply;
    
    // Play audio response
    if (data.audio_url) {
      if (currentAudio) { currentAudio.pause(); }
      currentAudio = new Audio(data.audio_url);
      currentAudio.play();
      setStatus('🔊 Speaking...', '');
      currentAudio.onended = () => setStatus('Click the mic and speak');
    } else {
      // Fallback: browser TTS
      const utterance = new SpeechSynthesisUtterance(reply);
      utterance.rate = 1.0;
      utterance.onend = () => setStatus('Click the mic and speak');
      setStatus('🔊 Speaking...');
      window.speechSynthesis.speak(utterance);
    }
  } catch(e) {
    setStatus('Error connecting. Try again.');
    btn.className = '';
    console.error(e);
  }
}

function toggleListen() {
  if (currentAudio) { currentAudio.pause(); currentAudio = null; }
  window.speechSynthesis.cancel();
  
  if (isListening) {
    recognition.stop();
    isListening = false;
    return;
  }
  
  recognition = initRecognition();
  if (!recognition) return;
  
  recognition.start();
  isListening = true;
  setStatus('🎙️ Listening... speak now', 'listening');
  transcriptEl.style.display = 'none';
  responseEl.style.display = 'none';
}

// Check if mic is available
navigator.mediaDevices?.getUserMedia({audio: true})
  .then(() => setStatus('Ready — click the mic to speak'))
  .catch(() => setStatus('⚠️ Please allow microphone access'));
</script>
</body>
</html>"""

@app.route('/')
def index():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    try:
        resp = requests.post(
            OPENCLAW_URL,
            headers={"Authorization": f"Bearer {OPENCLAW_TOKEN}", "Content-Type": "application/json"},
            json={
                "model": "anthropic/claude-sonnet-4-6",
                "messages": [
                    {"role": "system", "content": "You are Samantha, Alain's personal AI assistant. Be warm, direct, and concise — 1-3 sentences max. No markdown, just natural speech."},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 200
            },
            timeout=15
        )
        reply = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"reply": "Sorry, I'm having trouble connecting.", "audio_url": None})
    
    # Generate ElevenLabs audio
    audio_url = None
    try:
        tts_resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
            json={"text": reply, "model_id": "eleven_turbo_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
            timeout=10
        )
        if tts_resp.status_code == 200:
            # Save audio temporarily
            audio_path = "/tmp/samantha_response.mp3"
            with open(audio_path, 'wb') as f:
                f.write(tts_resp.content)
            audio_url = "/audio"
    except Exception:
        pass
    
    return jsonify({"reply": reply, "audio_url": audio_url})

@app.route('/audio')
def audio():
    try:
        with open("/tmp/samantha_response.mp3", 'rb') as f:
            data = f.read()
        return Response(data, mimetype='audio/mpeg')
    except:
        return "Not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
