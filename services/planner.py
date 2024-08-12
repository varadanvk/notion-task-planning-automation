from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from openai import OpenAI
import json
from datetime import datetime
import os
import pytz

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
    def parse_datetime(self, dt: Any) -> datetime:
        if isinstance(dt, str):
            return datetime.fromisoformat(dt.replace('Z', '+00:00'))
        elif isinstance(dt, dict):
            dt_str = dt.get('dateTime', dt.get('date', ''))
            tz_str = dt.get('timeZone', 'UTC')
            dt_obj = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return pytz.timezone(tz_str).localize(dt_obj)
        else:
            raise ValueError(f"Unsupported datetime format: {type(dt)}")
    
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
                end = due_date + timedelta(hours=1)  
                summary = event['Name']
            else:
                continue  

            event_prompt += f"- {summary} from {start.strftime('%Y-%m-%d %H:%M %Z')} to {end.strftime('%Y-%m-%d %H:%M %Z')}\n"
        
        event_prompt += "\nDO NOT SCHEDULE ANY EVENTS AT THE SAME TIME AS EXISTING ONES. MAKE SURE TO HAVE ALL EVENTS AFTER CURRENT DATE AND TIME. Try to leave AT LEAST a 15 minute gap in between events.\n\n"
        print(event_prompt)
        return event_prompt
    
    def create_calendar_events(self, notion_tasks: List[dict], upcoming_events: List[dict]) -> List[dict]:
        calendar_events = []
        temp_events = []
        calendar_context = self.generate_event_prompt(upcoming_events)
        
        print("Planning events...")
        
        for task in notion_tasks:
            prompt = f"""
            Please follow these scheduling guidelines:
            1. Schedule events between 9:00 AM and 11:59 PM (23:59) when possible, but you may schedule outside these hours if necessary.
            2. Try to leave at least a 15-minute gap between events, but shorter gaps are allowed if needed.
            3. Avoid overlapping with existing events when possible, but minor overlaps are acceptable if unavoidable.
            4. Schedule events after the current date and time ({self.get_current_datetime()}) unless the task is already overdue.
            5. For overdue tasks, schedule them as soon as reasonably possible.
            6. Consider the task's priority when scheduling. Higher priority tasks should generally be scheduled earlier, but this is not a strict rule. 
            7. Aim to schedule the event close to its due date when possible, but earlier scheduling is acceptable if needed.
            8. If you absolutely cannot schedule an event, explain why in your response.
            9. If a task is high or ASAP priority, ignore all other tasks/constraints and schedule it as soon as there is an opening.

            Task:
            Title: {task['Name']}
            Priority: {task['Priority']}
            Status: {task['Status']}
            Estimated Time: {task['Estimated Time']}
            Due Date: {task['Due date']}
            Activity: {task['Activity']}
            URL: {task['url']}

            Return a JSON object with keys: title, start, end, and description.
            
            Time format: YYYY-MM-DDTHH:MM:SSZ (Use 24-hour format)
            Description format: ACTIVITY: {task['Activity']}, PRIORITY: {task['Priority']}, DUE DATE: {task['Due date']}, ESTIMATED TIME: {task['Estimated Time']}, URL: {task['url']}
            
            Existing events (DO NOT SCHEDULE OVER THESE):
            {calendar_context}
            
            If you cannot schedule this task without violating the rules, respond with:
            {{
                "error": "Unable to schedule task due to constraints"
                "planned-time": "When the task was planned to be scheduled"
                "reason": "Reason why task cannot be scheduled"
            }}
            """
            
            #TODO: Implement short term memory for events just scheduled so that there are no overlaps
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a strict scheduling assistant. You MUST follow all scheduling rules precisely. Never make exceptions."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                
                event_data = json.loads(response.choices[0].message.content.strip())
                
                if "error" in event_data:
                    print(f"Scheduling error for task '{task['Name']}': {event_data['error']} \n Planned Time: {event_data['planned-time']} \n Reason: {event_data['reason']}")
                else:
                    print(f"Planned event: {event_data}")
                    calendar_events.append(event_data)
            except Exception as e:
                print(f"Error planning event: {str(e)}")
        
        print(f"Total events planned: {len(calendar_events)}")
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
            
            location_start = event['description'].find("LOCATION:")
            if location_start != -1:
                location_end = event['description'].find(",", location_start)
                if location_end != -1:
                    parsed_event['location'] = event['description'][location_start+9:location_end].strip()
            
            parsed_events.append(parsed_event)
        
        return parsed_events