import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ENV variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_REFERER = os.getenv("OPENROUTER_REFERER")
OPENROUTER_TITLE   = os.getenv("OPENROUTER_TITLE")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGORA_CREDENTIALS  = os.getenv("AGORA_CREDENTIALS")

AGORA_APPID        = os.getenv("AGORA_APP_ID")
AGORA_CHANNEL      = os.getenv("AGORA_CHANNEL")
AGORA_RTC_TOKEN    = os.getenv("AGORA_RTC_TOKEN")

# Agora join URL
url = f"https://api.agora.io/api/conversational-ai-agent/v2/projects/{AGORA_APPID}/join"

# Headers
headers = {
    "Authorization": f"Basic {AGORA_CREDENTIALS}",
    "Content-Type": "application/json"
}

# Build OpenRouter API key with headers included
merged_openrouter_key = (
    f"{OPENROUTER_API_KEY}; "
    f"HTTP-Referer={OPENROUTER_REFERER}; "
    f"X-Title={OPENROUTER_TITLE}"
)

# Payload
data = {
    "name": "MisSpoke",
    "properties": {
        "channel": AGORA_CHANNEL,
        "token": AGORA_RTC_TOKEN,
        "agent_rtc_uid": "0",
        "remote_rtc_uids": ["*"],
        "enable_string_uid": False,
        "idle_timeout": 120,

        # ---------------------------
        #        CUSTOM LLM
        # ---------------------------
        "llm": {
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "api_key": merged_openrouter_key,
            "system_messages": [
                {
                    "role": "system",
                    "content": "You are a helpful chatbot."
                }
            ],
            "greeting_message": "Hello, how can I help you?",
            "failure_message": "Sorry, I don't know how to answer this question.",
            "max_history": 10,
            "params": {
                "model": "qwen/qwen3-coder:free",
                "stream": True
            }
        },

        # ---------------------------
        #        ASR
        # ---------------------------
        "asr": {
            "language": "en-US"
        },

        # ---------------------------
        #        TTS
        # ---------------------------
        "tts": {
            "vendor": "elevenlabs",
            "params": {
                "key": ELEVENLABS_API_KEY,
                "model_id": "eleven_flash_v2_5",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "sample_rate": 24000
            }
        }
    }
}

# Make the request
response = requests.post(url, headers=headers, data=json.dumps(data))

print("Response Status:", response.status_code)
print("Response Body :", response.text)
