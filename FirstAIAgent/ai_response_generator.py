from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
print("Loaded key:", os.getenv("ANT_AP_KY"))
client = Anthropic(api_key = os.getenv("ANT_AP_KY"))

response = client.messages.create(
    model = "claude-sonnet-4-5-20250929",
    max_tokens = 150,
    messages = [{"role": "user", "content": "Compare the abilities of claude-3-sonnet and gpt-4 in detail."}]
)

print(response.content[0].text)



