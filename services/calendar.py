from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

class CalendarService:
    def __init__(self, credentials_path: str = 'token.json'):
        self.creds = Credentials.from_authorized_user_file(credentials_path, ['https://www.googleapis.com/auth/calendar'])
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_events(self, calendar_id: str = 'primary', time_min: str = None, max_results: int = 10) -> List[Dict[str, Any]]:
        if time_min is None:
            time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=time_min,
                                                   maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def parse_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse the list of events into a more readable format.

        :param events: List of event dictionaries or JSON string
        :return: List of parsed event dictionaries
        """
        # If events is a string, try to parse it as JSON
        if isinstance(events, str):
            try:
                events = json.loads(events)
            except json.JSONDecodeError:
                print("Error: Failed to parse events as JSON")
                return []

        # If events is not a list after JSON parsing, wrap it in a list
        if not isinstance(events, list):
            events = [events]
        
        parsed_events = []
        for event in events:
            parsed_event = {}
            
            # Handle start time
            if isinstance(event.get('start'), dict):
                parsed_event['start'] = event['start'].get('dateTime', event['start'].get('date'))
            elif isinstance(event.get('start'), str):
                parsed_event['start'] = event['start']
            
            # Handle end time
            if isinstance(event.get('end'), dict):
                parsed_event['end'] = event['end'].get('dateTime', event['end'].get('date'))
            elif isinstance(event.get('end'), str):
                parsed_event['end'] = event['end']
            
            # Handle summary/title
            parsed_event['summary'] = event.get('summary', event.get('title', 'Untitled Event'))
            
            # Handle location
            parsed_event['location'] = event.get('location', '')
            
            parsed_events.append(parsed_event)

        return parsed_events

    def add_event(self, event: Dict[str, Any], calendar_id: str = 'primary') -> Dict[str, Any]:
        return self.service.events().insert(calendarId=calendar_id, body=event).execute()

    def add_events(self, events: List[Dict[str, Any]], calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        added_events = []
        for event in events:
            added_event = self.add_event(event, calendar_id)
            added_events.append(added_event)
        return added_events