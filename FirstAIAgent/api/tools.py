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

@app.post("/gcal/delete_event")
async def delete_event(payload: Request):
    data = await payload.json()
    print("DELETE EVENT payload:", data)

    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=data["search_window_start"],
        timeMax=data["search_window_end"],
        q=data.get("search_summary"),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": "No matching events found"
            }
        )

    # Delete the first matching event
    event_to_delete = events[0]

    service.events().delete(
        calendarId="primary",
        eventId=event_to_delete["id"]
    ).execute()

    return JSONResponse({
        "status": "success",
        "deleted_event_id": event_to_delete["id"],
        "summary": event_to_delete.get("summary"),
        "start": event_to_delete["start"]
    })

@app.post("/gcal/move_event")
async def update_event(payload: Request):
    data = await payload.json()

    service = get_calendar_service()

    event_id = data["event_id"]

    # Fetch existing event
    event = service.events().get(
        calendarId="primary",
        eventId=event_id
    ).execute()

    # Update ONLY the time fields
    event["start"] = {
        "dateTime": data["start"]["dateTime"],
        "timeZone": data["start"]["timeZone"]
    }

    event["end"] = {
        "dateTime": data["end"]["dateTime"],
        "timeZone": data["end"]["timeZone"]
    }

    updated_event = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event
    ).execute()

    return JSONResponse({
        "status": "success",
        "event_id": updated_event["id"],
        "summary": updated_event.get("summary"),
        "start": updated_event["start"],
        "end": updated_event["end"],
        "html_link": updated_event["htmlLink"]
    })

@app.post("/gcal/add_reminder")
async def add_reminder(payload: Request):
    data = await payload.json()
    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=data["search_window_start"],
        timeMax=data["search_window_end"],
        q=data["search_summary"],
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "No matching event found"}
        )

    event = events[0]

    event["reminders"] = {
        "useDefault": False,
        "overrides": data["reminders"]
    }

    updated = service.events().update(
        calendarId="primary",
        eventId=event["id"],
        body=event
    ).execute()

    return JSONResponse({
        "status": "success",
        "event_id": updated["id"],
        "reminders": updated["reminders"]
    })
