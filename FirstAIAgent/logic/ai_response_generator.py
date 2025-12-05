from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key = os.getenv("ANT_AP_KY"))

SYSTEM_PROMPT = Path("system_prompt.txt").read_text()

# Function that grabs the Claude response with my own specifications
def get_claude_response(user_message: str):
    response = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        system = SYSTEM_PROMPT,
        max_tokens = 150,
        messages = [{"role": "user", "content": user_message}]

        return response.context[0].text
)




