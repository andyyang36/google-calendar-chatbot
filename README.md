
## Google Calendar Chatbot
---

Currently very functional but would love to turn this into a fullstack project and incorporate more language detection soon.

Inspired by YouTuber NeuralNine's video "Google Calendar Automation in Python", in the original version by NeuralNine, it retrieves the next 10 upcoming events from the user's primary calendar (starting from the current time). 

This project is an early-stage chatbot that interacts with Google Calendar. I have enhanced the foundation by modularizing the code and laying the groundwork for future improvements, including natural language command parsing. 

My goal is to enable users to schedule events through conversational commands—like "Schedule my dinner 3:00 pm ending at 5:00 pm tomorrow"—making calendar management more intuitive and accessible. 

The current implementation features spaCy natural language detection, secure OAuth 2.0 authentication, integration with the Google Calendar API, setting the stage for further expansion into a full-featured calendar management chatbot.

## Examples of Usage:  
---
Adding item to Calendar:  
<img width="668" alt="image" src="https://github.com/user-attachments/assets/40f64c60-c658-41b3-8964-b00d8a8c29a8" />

Removing item from Calendar:  
<img width="423" alt="image" src="https://github.com/user-attachments/assets/b0703d75-2a0b-40b9-a2de-1bca2b4fcb0b" />

Displaying Upcoming Events:  
<img width="286" alt="image" src="https://github.com/user-attachments/assets/4bd40f20-720e-4637-a3ff-d8af957fac40" />

## Features
---
Intelligent Natural Language Processing:
Uses spaCy to accurately parse natural language commands, extracting key details like dates, times, and event descriptions.

Seamless Google Calendar Integration:
Leverages the Google Calendar API to effortlessly create, modify, query, and delete events from your calendar.

Secure OAuth 2.0 Authentication:
Implements industry-standard OAuth 2.0 for secure authentication and authorization, protecting user data and ensuring privacy.

Flexible Event Scheduling:
Utilizes spaCy to extract key event details—such as the event description, date, time, and duration—from flexible natural language inputs like "Dinner with John 3 pm march 9," enabling intuitive scheduling.

User-Friendly Event Management:
Displays upcoming events with simple, sequential numbering for easy selection and management, streamlining your calendar workflow.

## File Descriptions
---
add.py This module processes natural language input to extract key event details such as date, time, duration, and event description. It leverages spaCy to identify DATE and TIME entities, and uses dateutil to parse and format the event’s start and end times. The module returns a dictionary containing the event summary, start datetime, and end datetime, which is then used by the main application to create an event via the Google Calendar API.

remove.py - Contains functionality to remove events from your Google Calendar. This module defines functions that, given a valid Calendar API service and an event ID, will delete the corresponding event from the user's primary calendar. It is integrated into the main application to provide a simple, user-friendly interface for event removal.

main.py - The main entry point of the application. This script handles user authentication with Google using OAuth 2.0, builds the Calendar API service, and provides a command-line interface for users to add, remove, or update calendar events. 

credentials.json - Where you put in your credentials from Google Cloud Console Credentials (Create project -> Select/Create a new one -> Enable Calendar API -> Create credentials -> Choose OAuth ID -> Export JSON)

requirements.txt - This file lists the Python packages required for the google-calendar-chatbot project. It includes dependencies for spaCy, Google Calendar API, and date parsing utilities. 


## Installation
---
1. Clone the Repository
git clone https://github.com/yourusername/google-calendar-chatbot.git

2. Change into the Project Directory
cd google-calendar-chatbot

3. Install the Dependencies
pip3 install -r requirements.txt

4. Import the Credentials
Download your OAuth 2.0 credentials from https://console.cloud.google.com/apis/credentials and save the JSON file as "credentials.json" in the project root.

5. Run the Application
python3 main.py

 


