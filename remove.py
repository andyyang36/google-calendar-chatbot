from googleapiclient.errors import HttpError

def remove_event(service, event_id):
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Event removed successfully.")
        return True
    except HttpError as error:
        print("An error occurred while removing the event:", error)
        return False
