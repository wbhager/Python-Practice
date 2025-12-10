from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path
import json
import requests
import os

load_dotenv()
client = Anthropic(api_key = os.getenv("ANT_AP_KY"))

SYSTEM_PROMPT = Path("templates/system_prompt.txt").read_text()

# Function that grabs the Claude response with my own specifications
def get_claude_response(user_message: str):
    raw = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        system = SYSTEM_PROMPT,
        max_tokens = 500,
        temperature = 0.7,
        messages = [{"role": "user", "content": user_message}])

    text = raw.content[0].text

    try:
        data = json.loads(text)
        if "tool" in data:
            tool = data["tool"]
            args = data.get("arguments", {})

            resp = requests.post(f"http://localhost:8000/tools/gcal/{tool.replace('gcal_', '')}", json=args)
            tool_result = resp.json()

            return f"Tool {tool} executed successfully. Result: {tool_result}"
    except:
        pass

    return text






