from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key = os.getenv("ANT_AP_KY"))

response = client.messages.create(
    model = "claude-3-sonnet-20250219",
    max_tokens = 100,
    messages = [{"role": "user", "content": "Compare the abilities of claude-3-sonnet and gpt-4 in detail."}]
)

print(response.content[0].text)


