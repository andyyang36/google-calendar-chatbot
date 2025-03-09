"""ADD FEATURE FOR PYTHON CHATBOT"""

import spacy
import sys


nlp = spacy.load("en_core_web_sm")

def check_exit(input_text):
    """Checks if the input is an exit command."""
    if input_text.upper() in ("EXIT", "CANCEL"):
        return True  
    return False

def is_valid_time(time_text):
    time_doc = nlp(time_text)
    for ent in time_doc.ents:
        if ent.label_ == "TIME":
            return True
    return False 

def get_date_from_user():
    """Checks if a valid date is entered"""
    while True: 
        date = input("Please enter a date (Example: March 9 2025): ")
        check_exit(date)
        date_doc = nlp(date)
        if is_valid_date(date):
            for date_ent in date_doc.ents:
                if date_ent.label_ == "DATE":
                    return date_ent.text
            else:
                print("You did not enter a valid date")

def is_valid_date(date_text):
    date_doc = nlp(date_text)
    for ent in date_doc.ents:
        if ent.label_ == "DATE":
            return True
        return False


def get_time_from_user():
    while True:
        time = input("Please enter a time: ")
        check_exit(time) #check for exit.
        if is_valid_time(time):
            time_doc = nlp(time)
            for time_ent in time_doc.ents:
                if time_ent.label_ == "TIME":
                    return time_ent.text
        else:
            print("You did not enter a valid time.")
def gather_info():
        text = input("Enter a date and a time for your event OR type 'EXIT' at any time to exit: ")
        check_exit(text)
        doc = nlp(text)
        command_time_exists = False
        command_date_exists = False
        event_date = None
        event_time = None

        """ABOVE takes in a input from the user, we have three minimum checkoffs and we can add some optional ones later"""

        for ent in doc.ents: #iterates through each entity
            if ent.label_ == "TIME": #ent label gives us the label, such as time, person, etc
                event_time = ent.text #ent text is the actual text of it. like 8 am. jennifer. etc.
                command_time_exists = True

            if ent.label_ == "DATE":
                event_date = ent.text
                command_date_exists = True

        """CHECKS IF DATE AND TIME EXISTS"""
        if not command_time_exists:
            event_time = get_time_from_user() 
            command_time_exists = True
        if not command_date_exists:            
            event_date = get_date_from_user()
            command_date_exists = True

        event_name = input("Description of your event: ")
        
        if command_time_exists and command_date_exists:    
            print(f"You have successfully scheduled {event_name} on {event_date} at {event_time}")
        
        
        return {
            "date": event_date,
            "time": event_time,
            "description": event_name,
        }

    
