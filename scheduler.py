from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

SCHEDULER_PROMPT = """
You are a personal assistant designed to manage your client's busy schedule. You are designed to build your client's day around their ideas for what they want to do. 
You will output JSON objects that represent the client's schedule for the day.

format for output:
event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

Do not use \n in the output.
"""

USER_PROMPT =""" 
I have a busy day ahead of me. Can you help me schedule my day? My plans are as follows:
Have lunch with a friend at 12:00 PM
Have a meeting at 2:00 PM
Pick up groceries at 4:00 PM
Do homework, have lunch, and some other things at 6:00 PM
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": SCHEDULER_PROMPT},
    {"role": "user", "content": USER_PROMPT}
  ]
)
# Deserialize the JSON string
parsed_json = json.loads(response.choices[0].message.content)

# Pretty print the JSON object
print(json.dumps(parsed_json, indent=2))

with open("schedule.json", "w") as f:
    f.write(json.dumps(parsed_json, indent=2))