from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os, json

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = FastAPI()

def get_calendar_service():
    """Handles token.json creation and builds Google Calendar service."""
    
    creds = None
    
    # If token.json exists, load it
    if os.path.exists("api/token.json"):
        creds = Credentials.from_authorized_user_file("api/token.json", SCOPES)
    
    # Otherwise ask user to authenticate in browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("api/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open("api/token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


@app.post("/gcal/add_event")
async def add_event(payload: Request):
    data = await payload.json()

    service = get_calendar_service()

    event_body = {
        "summary": data.get("summary"),
        "description": data.get("description", ""),
        "start": {
            "dateTime": data["start"]["dateTime"],
            "timeZone": data["start"]["timeZone"],
        },
        "end": {
            "dateTime": data["end"]["dateTime"],
            "timeZone": data["end"]["timeZone"],
        }
    }

    event = service.events().insert(calendarId="primary", body=event_body).execute()

    return JSONResponse({
        "status": "success",
        "event_id": event["id"],
        "html_link": event["htmlLink"]
    })


