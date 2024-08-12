from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import pytz

class CalendarService:
    def __init__(self, credentials_path: str = 'token.json'):
        self.creds = Credentials.from_authorized_user_file(credentials_path, ['https://www.googleapis.com/auth/calendar'])
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.timezone = pytz.timezone('America/Los_Angeles')

    def get_events(self, calendar_id: str = 'primary', time_min: str = None, max_results: int = 10) -> List[Dict[str, Any]]:
        if time_min is None:
            time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=time_min,
                                                   maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def parse_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse the list of events into a more readable format and handle time zone conversion.

        :param events: List of event dictionaries or JSON string
        :return: List of parsed event dictionaries
        """
        if isinstance(events, str):
            try:
                events = json.loads(events)
            except json.JSONDecodeError:
                print("Error: Failed to parse events as JSON")
                return []

        if not isinstance(events, list):
            events = [events]
        
        parsed_events = []
        for event in events:
            parsed_event = {}
            
            # Handle start time
            start_time, start_tz = self._parse_datetime(event.get('start'))
            parsed_event['start'] = {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': start_tz
            }
            
            # Handle end time
            end_time, end_tz = self._parse_datetime(event.get('end'))
            parsed_event['end'] = {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': end_tz
            }
            
            # Handle summary/title
            parsed_event['summary'] = event.get('summary', event.get('title', 'Untitled Event'))
            
            # Handle description
            parsed_event['description'] = event.get('description', '')
            
            # Handle location
            parsed_event['location'] = event.get('location', '')
            
            # Handle reminders
            parsed_event['reminders'] = event.get('reminders', {'useDefault': True})
            
            parsed_events.append(parsed_event)

        return parsed_events

    def _parse_datetime(self, dt_dict: Dict[str, Any]) -> tuple:
        """
        Parse datetime from event dictionary and handle time zone conversion.

        :param dt_dict: Dictionary containing dateTime and timeZone
        :return: Tuple of (datetime object, time zone string)
        """
        if isinstance(dt_dict, dict):
            dt_str = dt_dict.get('dateTime', dt_dict.get('date'))
            tz_str = dt_dict.get('timeZone', 'UTC')
        elif isinstance(dt_dict, str):
            dt_str = dt_dict
            tz_str = 'UTC'
        else:
            raise ValueError("Invalid datetime format")

        # Parse the datetime string
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))

        # If the datetime is in UTC, convert it to the specified time zone
        if dt.tzinfo == pytz.UTC:
            local_tz = pytz.timezone(tz_str)
            dt = dt.astimezone(local_tz)
            tz_str = str(local_tz)

        return dt, tz_str

    def add_event(self, event: Dict[str, Any], calendar_id: str = 'primary') -> Dict[str, Any]:
        # Parse the event before adding it to ensure correct time zone handling
        parsed_events = self.parse_events([event])
        if parsed_events:
            return self.service.events().insert(calendarId=calendar_id, body=parsed_events[0]).execute()
        else:
            raise ValueError("Failed to parse event")
    def add_events(self, events: List[Dict[str, Any]], calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        added_events = []
        for event in events:
            added_event = self.add_event(event, calendar_id)
            added_events.append(added_event)
        return added_events