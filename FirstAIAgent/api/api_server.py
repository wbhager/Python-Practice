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



@app.post("/tools/gcal/add_event")
async def add_event(payload: Request):
    data = await payload.json()
    # TODO: Replace with real GCal logic
    return JSONResponse({
        "status": "stubbed-success",
        "event_id": "fake_12345",
        "html_link": "https://calendar.google.com/event?eid=fake"
    })

@app.post("/tools/gcal/delete_event")
async def delete_event(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "deleted": True,
        "notes": "This is a stub. No actual deletion performed."
    })

@app.post("/tools/gcal/list_events")
async def list_events(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "events": [
            {
                "event_id": "fake_id_1",
                "summary": "Stub Event 1",
                "start": "2025-12-13T10:00:00-05:00",
                "end":   "2025-12-13T11:00:00-05:00"
            }
        ]
    })

@app.post("/tools/gcal/add_reminder")
async def add_reminder(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "reminder_id": "fake_reminder_1"
    })
