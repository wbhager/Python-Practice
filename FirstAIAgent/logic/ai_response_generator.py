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

    print("----- RAW CLAUDE TEXT -----")
    print(text)
    print("---------------------------")

    text = raw.content[0].text

    # CLEAN HERE — BEFORE json.loads(text)
    clean = (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

    print("CLEANED TEXT:", clean)

    try:
        data = json.loads(clean)
        print("JSON PARSED SUCCESSFULLY:")
        print(data)

        if "tool" in data:
            print("TOOL CALL DETECTED:", data["tool"])
            tool = data["tool"]
            args = data.get("arguments", {})
            print("TOOL ARGUMENTS:", args)

            # Clean tool name fully
            clean_tool = tool.strip().lower()

            # Map tools directly to endpoints (safe + explicit)
            endpoint_map = {
                "gcal_add_event": "add_event",
                "gcal_delete_event": "delete_event",
                "gcal_list_events": "list_events",
                "gcal_add_reminder": "add_reminder"
            }

            if clean_tool not in endpoint_map:
                print("UNKNOWN TOOL:", clean_tool)
                return "ERROR: Unknown tool call"

            endpoint = endpoint_map[clean_tool]

            resp = requests.post(
                f"http://localhost:8100/gcal/{endpoint}",
                json=args
            )

            print("TOOL ENDPOINT RESPONSE RAW:", resp.text)

            resp_json = resp.json()

            return {
                "tool_executed": tool,
                "result": resp_json
            }

    except Exception as e:
        print("JSON FAILED TO PARSE:", e)

    print("NO TOOL CALL — returning raw text")
    return text