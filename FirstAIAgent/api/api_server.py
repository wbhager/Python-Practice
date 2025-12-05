from fastapi import FastAPI
from pydantic import BaseModel
from logic.ai_response_generator import client

app = FastAPI()

class Message(BaseModel):
    message: str

#Creating api endpoint,
##### Note: user represents user talking to model, assistant represents referencing previous prompt responses, system is system prompts
@app.post("/chat")
async def chat_endpoint(data: Message):
    user_message = data.message

    response = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        max_tokens = 500,
        messages = [{"role": "user", "content": user_message}]
    )

    reply = response.content[0].text

    return {"reply": reply}


