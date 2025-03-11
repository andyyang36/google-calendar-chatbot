import os.path
import datetime as dt
import add
import remove

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def display_upcoming_events(service):
    now = dt.datetime.utcnow().isoformat() + "Z"
    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get('items', [])
        if not events:
            print("No upcoming events found.")
        else:
            print("Upcoming 5 events:")
            for idx, event in enumerate(events):
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No Title')
                print(f"{idx+1}. {start} - {summary} (ID: {event['id']})")
    except HttpError as error:
        print("An error occurred while fetching events:", error)

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
    except HttpError as error:
        print("An error occurred while creating the service:", error)
        return

    while True:
        print("\nActions:")
        print("1. Add an event to my calendar")
        print("2. Remove an event from my calendar")
        print("3. View upcoming events on my calendar")
        print("4. Exit")
        user_action = input("What would you like to do?: ").strip()

        if user_action == "1":
            try:
                event_details = add.gather_info()
                if event_details is None:
                    print("Invalid event details provided.")
                    continue
                event_dict = {
                    'summary': event_details['summary'],
                    'start': {'dateTime': event_details['start'].isoformat(), 'timeZone': "America/New_York"},
                    'end': {'dateTime': event_details['end'].isoformat(), 'timeZone': "America/New_York"}
                }
                created_event = service.events().insert(calendarId="primary", body=event_dict).execute()
                print("Event created successfully.")
            except HttpError as error:
                print("An error occurred while adding the event:", error)

        elif user_action == "2":
            try:
                display_upcoming_events(service)
                event_id = input("Enter the event ID you want to remove: ").strip()
                if not event_id:
                    print("No event ID provided.")
                    continue
                if remove.remove_event(service, event_id):
                    pass
                else:
                    print("Failed to remove event.")
            except HttpError as error:
                print("An error occurred while removing the event:", error)
        elif user_action == "3":
            display_upcoming_events(service)


        elif user_action == "4":
            print("Exiting... ")
            break

        else:
            print("Invalid option. Please choose a valid action.")

if __name__ == '__main__':
    main()
