import os.path  #checks for file existence
import datetime as dt #date time
import add


from google.auth.transport.requests import Request #purpose is to get new login
from google.oauth2.credentials import Credentials #oauth credentials to communicate between google api and here
from google_auth_oauthlib.flow import InstalledAppFlow #key that allows program to use your google account
from googleapiclient.discovery import build #allows you to access google calendar so you can read,add, update events
from googleapiclient.errors import HttpError #safety net, lets your program know the mistake instead of crashing

SCOPES = ["https://www.googleapis.com/auth/calendar"] #scope is the level of permission being requested

def main():
    creds = None #initializes it as none to start

    if os.path.exists("token.json"): #checks curr directory for token.json
        creds = Credentials.from_authorized_user_file("token.json", SCOPES) 

    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    print("Actions:")
    print("1. Add a event to my calendar")
    user_action = input("What would you like to do?: ")
    if user_action == "1":
        try:
            service = build("calendar", "v3", credentials=creds)
            now = dt.datetime.now().isoformat() + "Z"
            event_details = add.gather_info()
            if event_details is None:
                print("Invalid")
                return
            else:
                event_dict = {
                    'summary': event_details['summary'],
                    'start': {'dateTime': event_details['start'].isoformat(), 'timeZone':"America/New_York"},
                    'end': {'dateTime': event_details['end'].isoformat(), 'timeZone': "America/New_York"}
                }
            created_event = service.events().insert(calendarId="primary",body=event_dict).execute()
            created_event = service.events().insert(calendarId="primary", body=event_dict).execute()
            print("Created Event:", created_event)


        except HttpError as error:
            print("An error occurred: ", error)
        
        

if __name__ == '__main__':
    main()
