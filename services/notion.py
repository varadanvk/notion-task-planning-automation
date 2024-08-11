import requests
import json
import os
from typing import List, Dict, Any

class NotionDatabaseManager:
    def __init__(self, database_id: str, token: str = None):
        self.database_id = database_id
        self.token = token or os.environ.get('NOTION_TOKEN')
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def query_database(self, filter_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.base_url}/databases/{self.database_id}/query"
        data = {
            "filter": {
                "or": filter_conditions
            }
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def get_tasks_by_status(self, statuses: List[str]) -> Dict[str, Any]:
        filter_conditions = [
            {
                "property": "Status",
                "status": {
                    "equals": status
                }
            } for status in statuses
        ]
        return self.query_database(filter_conditions)

    def save_results_to_file(self, data: Dict[str, Any], filename: str = 'notion_results.json'):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def parse_notion_response(self, response: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Parse the Notion API response and extract important properties for multiple tasks.
        
        :param response: The full Notion API response
        :return: A list of dictionaries, each containing the simplified data for a task
        """
        parsed_tasks = []
        
        if not response.get('results'):
            return parsed_tasks
        
        for task in response['results']:
            properties = task['properties']
            
            parsed_task = {
                "Name": properties['Name']['title'][0]['text']['content'] if properties['Name']['title'] else "",
                "Status": properties['Status']['status']['name'] if properties['Status']['status'] else "",
                "Priority": properties['Priority']['select']['name'] if properties['Priority']['select'] else "",
                "Estimated Time": properties['Estimated Time']['rich_text'][0]['text']['content'] if properties['Estimated Time']['rich_text'] else "",
                "Due date": properties['Due date']['date']['start'] if properties['Due date']['date'] else "",
                "Activity": properties['Rollup']['rollup']['array'][0]['title'][0]['text']['content'] if properties['Rollup']['rollup']['array'] else "",
                "url": task['url'],
            }
            
            parsed_tasks.append(parsed_task)
        
        return parsed_tasks