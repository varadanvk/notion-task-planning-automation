import json
import os
from services.notion import NotionDatabaseManager
from services.calendar import CalendarService
from services.planner import Planner
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

def query_database(database_id: str, statuses: List[str]) -> Dict[str, Any]:
    ndm = NotionDatabaseManager(database_id)
    results = ndm.get_tasks_by_status(statuses)
    print(json.dumps(results, indent=2))
    ndm.save_results_to_file(results, 'notion_results.json')
    return results
    
def main():
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID environment variable is not set")
    
    ndm = NotionDatabaseManager(database_id=database_id)
    planner = Planner(timezone="America/Los_Angeles")
    calendar = CalendarService()
    statuses = ["In Progress", "Not Started"]
    
    # Query and parse Notion tasks
    tasks = query_database(database_id, statuses)
    parsed_tasks = ndm.parse_notion_response(tasks)
    print(f"Number of parsed tasks: {len(parsed_tasks)}")
    print("Parsed tasks:")
    print(json.dumps(parsed_tasks, indent=2))
    
    # Get upcoming events from Calendar
    try:
        upcoming_events = calendar.get_events()
        print(f"Number of upcoming events: {len(upcoming_events)}")
        print("Upcoming events (raw):")
        print(json.dumps(upcoming_events, indent=2))
        
        parsed_upcoming_events = calendar.parse_events(upcoming_events)
        print(f"Number of parsed upcoming events: {len(parsed_upcoming_events)}")
        print("\nParsed upcoming events:")
        print(json.dumps(parsed_upcoming_events, indent=2))
        
        for event in parsed_upcoming_events:
            print(event['start'], event['summary'])
    except Exception as e:
        print(f"Error processing upcoming events: {str(e)}")
        parsed_upcoming_events = []
        
    # Convert Notion tasks to calendar events, considering existing events
    if(1+1==2):
        if not parsed_tasks:
            print("No tasks to plan")
        elif not parsed_upcoming_events:
            print("No upcoming events to consider")
        
        planned_events = planner.create_calendar_events(parsed_tasks, parsed_upcoming_events)
        print(f"Number of planned events: {len(planned_events)}")
        print("\nPlanned events:")
        print(json.dumps(planned_events, indent=2))
        
        if not planned_events:
            print("No events were planned. Check the Planner.create_calendar_events method.")
            return
        
        # Parse the planned events
        parsed_planned_events = planner.parse_planner_response(planned_events)
        
        print("\Parsed Planned events:")
        print(json.dumps(parsed_planned_events, indent=2))
        
        # Save calendar events to file
        with open('calendar_events.json', 'w') as f:
            json.dump(parsed_planned_events, f, indent=2)

        # Add events to calendar
        calendar.add_events(parsed_planned_events)

    # except Exception as e:
    #     print(f"Error creating calendar events: {str(e)}")
        
if __name__ == "__main__":
    main()