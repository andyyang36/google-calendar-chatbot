"""ADD FEATURE FOR PYTHON CHATBOT"""

import spacy
import sys
from dateutil import parser  # used to parse dates and times

nlp = spacy.load("en_core_web_sm")

def check_exit(input_text):
    if input_text.upper() in ("EXIT", "CANCEL"):
        return True
    return False

def is_valid_time(time_text):

    time_doc = nlp(time_text)
    for ent in time_doc.ents:
        if ent.label_ == "TIME":
            return True
    return False 

def is_valid_date(date_text):
    date_doc = nlp(date_text)
    for ent in date_doc.ents:
        if ent.label_ == "DATE":
            return True
    return False

def get_date_from_user():

    while True: 
        date = input("Please enter a date (Example: March 9 2025): ")
        check_exit(date)
        if is_valid_date(date):
            date_doc = nlp(date)
            for ent in date_doc.ents:
                if ent.label_ == "DATE":
                    return ent.text
        else:
            print("You did not enter a valid date.")

def get_time_from_user():
    while True:
        time = input("Please enter a time: ")
        check_exit(time)
        if is_valid_time(time):
            time_doc = nlp(time)
            for ent in time_doc.ents:
                if ent.label_ == "TIME":
                    return ent.text
        else:
            print("You did not enter a valid time.")

def parse_event_datetime(date_str, time_str):
    combined = f"{date_str} {time_str}"
    try:
        dt_obj = parser.parse(combined)
        return dt_obj.isoformat()
    except ValueError:
        print("Could not parse the date and time. Please check your input.")
        return None

def gather_info():

    text = input("Enter a date and a time for your event OR type 'EXIT' at any time to exit: ")
    check_exit(text)
    doc = nlp(text)
    
    command_time_exists = False
    command_date_exists = False
    event_date = None
    event_time = None

    for ent in doc.ents:
        if ent.label_ == "TIME":
            event_time = ent.text
            command_time_exists = True
        if ent.label_ == "DATE":
            event_date = ent.text
            command_date_exists = True

    if not command_time_exists:
        event_time = get_time_from_user()
        command_time_exists = True
    if not command_date_exists:
        event_date = get_date_from_user()
        command_date_exists = True

    event_name = input("Description of your event: ")
    
    parsed_datetime = parse_event_datetime(event_date, event_time)
    if parsed_datetime is None:
        print("There was an error parsing the date and time.")
    else:
        print(f"You have successfully scheduled '{event_name}' on {event_date} at {event_time}")

    return {
        "date": event_date,
        "time": event_time,
        "iso_datetime": parsed_datetime,
        "description": event_name,
    }

if __name__ == '__main__':
    event_details = gather_info()
    print("Parsed event details:", event_details)
