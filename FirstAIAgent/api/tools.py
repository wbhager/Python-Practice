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

@app.post("/gcal/update_event")
async def update_event(payload: Request):
    data = await payload.json()

    print("UPDATE_EVENT RAW PAYLOAD:", data)
    print("Keys received:", data.keys())

    service = get_calendar_service()

    print("Searching with:",
          data.get("search_window_start"),
          data.get("search_window_end"),
          data.get("search_summary"))

    events = service.events().list(
        calendarId="primary",
        timeMin=data["search_window_start"],
        timeMax=data["search_window_end"],
        q=data.get("search_summary"),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    if not events:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "No matching event found"}
        )

    event = events[0]

    updated_event = service.events().patch(
        calendarId="primary",
        eventId=event["id"],
        body={
            "start": data["new_start"],
            "end": data["new_end"]
        }
    ).execute()

    return JSONResponse({
        "status": "success",
        "event_id": event["id"],
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

@app.post("/gcal/list_events")
async def list_events(payload: Request):
    data = await payload.json()
    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=data["time_min"],
        timeMax=data["time_max"],
        maxResults=int(data.get("max_results", 10)),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    items = events_result.get("items", [])

    # Return only what you care about (keeps n8n + Claude simpler)
    events = []
    for e in items:
        start = e.get("start", {})
        end = e.get("end", {})
        events.append({
            "id": e.get("id"),
            "summary": e.get("summary", "(no title)"),
            "start": start.get("dateTime") or start.get("date"),
            "end": end.get("dateTime") or end.get("date"),
            "html_link": e.get("htmlLink", "")
        })

    return JSONResponse({
        "status": "success",
        "count": len(events),
        "events": events
    })
