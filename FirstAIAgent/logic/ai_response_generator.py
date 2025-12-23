from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path
import json
import requests
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANT_AP_KY"))

SYSTEM_PROMPT = Path("templates/system_prompt.txt").read_text()
STR_TOOL_OUTPUT_SP = Path("templates/structuredToolOutput_sysPrompt.txt").read_text()

endpoint_map = {
    "gcal_add_event": "add_event",
    "gcal_delete_event": "delete_event",
    "gcal_list_events": "list_events",
    "gcal_add_reminder": "add_reminder",
    "gcal_update_event": "update_event",
    "gcal_give_schedule_advice": "give_schedule_advice"
}

def get_claude_response(user_message: str, system_prompt: str):
    raw = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        system=system_prompt,
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": user_message}],
    )

    text = raw.content[0].text

    clean = (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

    # Try parse JSON (tool call or formatter output)
    try:
        data = json.loads(clean)
    except Exception:
        # If it's not JSON, return as plain reply JSON
        return {"reply": clean}

    # If this prompt is the formatter prompt, it should already return {"reply": "..."}
    # Just pass it back.
    if "reply" in data and "tool" not in data:
        return data

    # Otherwise, this is the tool-calling prompt case
    if "tool" in data:
        tool = data["tool"].strip().lower()
        args = data.get("arguments", {})

        if tool not in endpoint_map:
            return {"reply": f"ERROR: Unknown tool call '{tool}'"}

        endpoint = endpoint_map[tool]

        resp = requests.post(
            f"http://localhost:8100/gcal/{endpoint}",
            json=args,
            timeout=30,
        )

        # If tool server errors, return that cleanly
        try:
            resp_json = resp.json()
        except Exception:
            return {"reply": f"Tool error: {resp.text}"}

        return {
            "tool_executed": tool,
            "result": resp_json
        }

    # If it was JSON but not tool/reply, fallback
    return {"reply": clean}
