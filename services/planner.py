from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from openai import OpenAI
import json
from datetime import datetime
import os

class NotionTask(BaseModel):
    Name: str
    Status: str
    Priority: str
    Estimated_Time: Optional[str]
    Due_date: str
    Activity: str
    url: str

class CalendarEvent(BaseModel):
    title: str
    start: str
    end: str
    description: str

class Planner:
    def __init__(self, api_key: Optional[str] = None, timezone: str = "America/Los_Angeles"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.timezone = "America/Los_Angeles"

    def get_current_datetime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    def parse_datetime(self, dt: str) -> datetime:
        return datetime.fromisoformat(dt)
    
    def generate_event_prompt(self, events: List[Dict[str, Any]]) -> str:
        current_time = self.get_current_datetime()
        event_prompt = f"Current date and time: {current_time}\n\n"
        event_prompt += "Here are the upcoming events that you cannot schedule over:\n\n"
        for event in events:
            if 'start' in event and 'end' in event:
                # This is an existing calendar event
                start = self.parse_datetime(event['start'])
                end = self.parse_datetime(event['end'])
                summary = event.get('summary', 'Unnamed Event')
            elif 'Due_date' in event:
                # This is a task to be scheduled
                due_date = self.parse_datetime(event['Due_date'])
                start = due_date
                end = due_date + timedelta(hours=1)  # Assume 1 hour duration if not specified
                summary = event['Name']
            else:
                continue  # Skip events that don't match either format

            event_prompt += f"- {summary} from {start.strftime('%Y-%m-%d %H:%M %Z')} to {end.strftime('%Y-%m-%d %H:%M %Z')}\n"
        
        event_prompt += "\DO NOT SCHEDULE ANY EVENTS AT THE SAME TIME AS EXISTING ONES. MAKE SURE TO HAVE ALL EVENTS AFTER CURRENT DATE AND TIME. Try to leave AT LEAST a 15 minute gap in between events.\n\n"
        print(event_prompt)
        return event_prompt
    
    def create_calendar_events(self, notion_tasks: List[dict], upcoming_events: List[dict]) -> List[dict]:
        calendar_events = []
        
        calendar_context = self.generate_event_prompt(upcoming_events)
        
        for task in notion_tasks:
            prompt = f"""
            Convert the following task into a calendar event JSON format:

            Task:
            Title: {task['Name']}
            Priority: {task['Priority']}
            Status: {task['Status']}
            Estimated Time: {task['Estimated Time']}
            Due Date: {task['Due date']}
            Activity: {task['Activity']}
            URL: {task['url']}

            Return a JSON object with keys: title, start, end, and description.
            
            Formatting for time: YYYY-MM-DDTHH:MM:SSZ 
            Formatting for description: ACTIVITY: PRIORITY: {task['Priority']}, {task['Activity']}, DUE DATE: {task['Due date']},  URL: {task['url']}, ESTIMATED TIME: {task['Estimated Time']}, MORE INFO: {task['url']}
            
            """
            
            response = self.client.chat.completions.create(
                    model="gpt-4o",  # Make sure this is the correct model name
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that creates a schedule for the user based on their time and availability. Respond with a JSON object for a single calendar event with fields: title, start, end, and description."},
                        {"role": "assistant", "content": calendar_context},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
            
            # Parse the response as JSON
            event_data = json.loads(response.choices[0].message.content.strip())
            calendar_events.append(event_data)
        
        return calendar_events
    
    def parse_planner_response(self, ai_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_events = []
        for event in ai_events:
            parsed_event = {
                'summary': event['title'],
                'description': event['description'],
                'start': {
                    'dateTime': event['start'],
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': event['end'],
                    'timeZone': 'America/Los_Angeles',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            # Extract location if it's in the description
            location_start = event['description'].find("LOCATION:")
            if location_start != -1:
                location_end = event['description'].find(",", location_start)
                if location_end != -1:
                    parsed_event['location'] = event['description'][location_start+9:location_end].strip()
            
            parsed_events.append(parsed_event)
        
        return parsed_events