import requests
import os
from dotenv import load_dotenv

load_dotenv()

AGORA_CREDENTIALS = os.getenv("AGORA_CREDENTIALS")
AGORA_APP_ID = os.getenv("AGORA_APP_ID")

# INSERT the agent ID you want to stop
AGENT_ID = "A42AK43RK42AK24TF55XF64JN27RK67H"  # <-- change this each time

url = f"https://api.agora.io/api/conversational-ai-agent/v2/projects/{AGORA_APP_ID}/agents/{AGENT_ID}/leave"

headers = {
    "Authorization": f"Basic {AGORA_CREDENTIALS}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers)

print("Status:", response.status_code)
print("Body:", response.text)
