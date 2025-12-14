from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = FastAPI()

@app.post("/gcal/add_event")
async def add_event(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "event_id": "fake_12345",
        "html_link": "https://calendar.google.com/event?eid=fake"
    })

@app.post("/gcal/delete_event")
async def delete_event(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "deleted": True
    })

@app.post("/gcal/list_events")
async def list_events(payload: Request):
    data = await payload.json()
    return JSONResponse({
        "status": "stubbed-success",
        "events": [
            {
                "event_id": "fake_id_1",
                "summary": "Stub Event 1",
                "start": "2025-12-13T10:00:00",
                "end": "2025-12-13T11:00:00"
            }
        ]
    })