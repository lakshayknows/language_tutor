import json
import requests
import os

class EventHandler:

    def __init__(self):
        self.groq_api = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY")

    def handle_event(self, event_type, data):
        print(f"[EVENT] {event_type}")

        if event_type == "asr.message.received":
            user_text = data.get("text", "")
            return self.process_user_text(user_text)

        elif event_type == "agent.response.completed":
            print("Agent finished speaking.")

        elif event_type == "call.started":
            print("Call has started.")

        elif event_type == "call.ended":
            print("Call has ended.")

        else:
            print(f"Unhandled event: {event_type}")

        return None

    def process_user_text(self, text: str):
        """
        Takes raw ASR text → sends to LLM → returns structured response for tutor.
        """

        print(f"[USER SAID] {text}")

        # Build message payload
        messages = [
            {"role": "system", "content": "You are an adaptive, gentle language tutor. Correct mistakes, explain briefly, ask a follow-up question."},
            {"role": "user", "content": text}
        ]

        payload = {
            "model": "openai/gpt-oss-120b",
            "messages": messages,
            "stream": False
        }

        # Call Groq LLM
        response = requests.post(
            self.groq_api,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )

        if response.status_code != 200:
            print("[LLM ERROR]", response.text)
            return {"type": "agent.response", "text": "I'm having trouble understanding that. Can you try again?"}

        # Parse response
        llm_output = response.json()["choices"][0]["message"]["content"]
        print("[LLM OUTPUT]", llm_output)

        # Return formatted agent response
        return {
            "type": "agent.response",
            "text": llm_output
        }
