from fastapi import FastAPI
from pydantic import BaseModel
from logic.ai_response_generator import get_claude_response

app = FastAPI()

class Message(BaseModel):
    message: str

# Creating api endpoint, handles the post request and routing
@app.post("/chat")
async def chat_endpoint(data: Message):
    user_message = get_claude_response(data.message)
    return {"reply": reply}


