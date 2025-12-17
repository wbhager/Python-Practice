from fastapi import FastAPI, Request
from pydantic import BaseModel
from logic.ai_response_generator import get_claude_response
import json
import requests

from fastapi.responses import JSONResponse

app = FastAPI()

class Message(BaseModel):
    message: str

# Creating api endpoint, handles the post request and routing
@app.post("/chat")
async def chat_endpoint(data: Message):
    reply = get_claude_response(data.message)
    return {"reply": reply}




