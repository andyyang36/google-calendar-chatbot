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
            return {}
        else:
            print("Upcoming 5 events:")
            event_mapping = {}  # Map displayed number to actual event ID
            for idx, event in enumerate(events):
                start_val = event['start'].get('dateTime', event['start'].get('date'))
                try:
                    dt_obj = dt.datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                    start_formatted = dt_obj.strftime("%b %d, %Y %I:%M %p")
                except Exception:
                    start_formatted = start_val
                summary = event.get('summary', 'No Title')
                counter = idx + 1
                event_mapping[counter] = event['id']
                print(f"{counter}. {start_formatted} - {summary}")
            return event_mapping
    except HttpError as error:
        print("An error occurred while fetching events:", error)
        return {}

def parse_command(user_input):
    """
    Map natural language commands to a menu option based on keyword matching.
    This uses a list of tuples containing lists of keywords and their corresponding action.
    """
    commands_list = [
        (["schedule", "meeting", "make", "add event", "create", "organize"], "1"),
        (["remove", "delete", "cancel event"], "2"),
        (["view", "upcoming", "show events", "events", "coming", "list"], "3"),
        (["exit", "quit", "close", "nevermind", "leave"], "4")
    ]
    
    command_text = user_input.lower()
    
    for keywords, option in commands_list:
        if any(keyword in command_text for keyword in keywords):
            return option

    # If no keywords match, assume the user entered a direct menu number.
    return user_input

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

        print('Examples: "Schedule a meeting", "Delete an event", "Show me my upcoming events": ')
    
        user_action_input = input("What would you like to do?: ").strip()        
        user_action = parse_command(user_action_input)

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
                mapping = display_upcoming_events(service)
                if not mapping:
                    continue
                selection = input("Enter the number of the event you want to remove: ").strip()
                try:
                    selection = int(selection)
                    event_id = mapping.get(selection)
                    if not event_id:
                        print("Invalid selection.")
                        continue
                    if remove.remove_event(service, event_id):
                        print("Event removed successfully.")
                    else:
                        print("Failed to remove event.")
                except ValueError:
                    print("Please enter a valid number.")
            except HttpError as error:
                print("An error occurred while removing the event:", error)
        elif user_action == "3":
            display_upcoming_events(service)
            print("\n")
        elif user_action == "4":
            print("Exiting... ")
            break
        else:
            print("Invalid option. Please choose a valid action.")

if __name__ == '__main__':
    main()
