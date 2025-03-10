import spacy
import sys
from dateutil import parser, tz
import datetime as dt
import re


nlp = spacy.load("en_core_web_sm")


def check_exit(input_text):
    if input_text.upper() in ("EXIT", "CANCEL"):
        sys.exit()
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
        local_tz = tz.gettz()
        dt_obj = dt_obj.replace(tzinfo=local_tz)
        return dt_obj  
    except ValueError:
        print("Could not parse the date and time. Please check your input.")
        return None

def gather_info():
    text = input("Enter a date, time and description for your event: ")
    check_exit(text)
    doc = nlp(text)
    
    event_date = None
    event_time = None
    event_length = None
    command_time_exists = False  
    command_date_exists = False

    for ent in doc.ents:
        if ent.label_ == "TIME":
            event_time = ent.text
            command_time_exists = True
        if ent.label_ == "DATE":
            event_date = ent.text
            command_date_exists = True

    if not command_time_exists:
        event_time = get_time_from_user()
    if not command_date_exists:
        event_date = get_date_from_user()


    start_dt = parse_event_datetime(event_date, event_time)
    while start_dt is None:
        event_date = input("Enter a date: ")
        start_dt = parse_event_datetime(event_date, event_time)
        print("Error parsing date and time, try again")

    event_name = text.replace(event_date, "").replace(event_time, "").replace("on","").replace("at","").strip()
    event_name = re.sub(r"\b\d{4}\b", "", event_name).strip()

    while True:
        event_length_str = input("How long is your event? (Enter in minutes): ")
        check_exit(event_length_str)
        try:
            event_length = float(event_length_str)
            if event_length <= 0:
                print("Invalid Event Length. Must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the duration.")

    end_dt = start_dt + dt.timedelta(minutes=event_length)
    print(f"You have successfully scheduled '{event_name}' on {event_date} at {event_time} for {event_length} minutes.")



    return {
        'summary': event_name,
        'start': start_dt,
        'end': end_dt
    }
