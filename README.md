# AI Scheduler

AI Scheduler is an intelligent task management and scheduling system that integrates Notion tasks with Google Calendar using AI-powered planning.

## Features

- Fetch tasks from Notion database
- Retrieve existing events from Google Calendar
- AI-powered scheduling of tasks considering existing commitments
- Automatic creation of calendar events based on planned schedule
- Flexible parsing of different event formats
- Timezone-aware scheduling

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- A Notion account with API access
- A Google account with Calendar API enabled

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/ai-scheduler.git
   cd ai-scheduler
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:

   - Create a `.env` file in the project root
   - Add the following variables:

     ```
     NOTION_TOKEN=your_notion_api_token
     OPENAI_API_KEY=your_openai_api_key
     NOTION_DATABASE_ID=your_notion_db
     CALENDAR_ACCOUNT=calendar_account_you_use

     ```

4. Set up Google Calendar API:
   - Follow the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python) to enable the API and download your `credentials.json` file
   - Place the `credentials.json` file in the project root

## Usage

1. Update the `database_id` in `main.py` with your Notion database ID. You can find your database id in the link that is what comes up when you open the page that is your database

   - Example: https://www.notion.so/varadankalkunte/52954ca0e3c34a69bb013908f6def012
   - The ID in this case is `52954ca0e3c34a69bb013908f6def012`

2. Run the main script:

   ```
   python main.py
   ```

3. The script will:

   - Fetch tasks from your Notion database
   - Retrieve upcoming events from your Google Calendar
   - Use AI to plan a schedule for your tasks
   - Generate new calendar events for the planned tasks
   - Save the planned events to a JSON file

4. Review the generated `calendar_events.json` file to see the planned schedule.

5. Uncomment the relevant line in `main.py` to automatically add the events to your Google Calendar.

## Project Structure

- `main.py`: The entry point of the application
- `services/`:
  - `notion.py`: Handles interaction with the Notion API
  - `calendar.py`: Manages Google Calendar operations
  - `planner.py`: Contains the AI planning logic

## Contributing

Contributions to the AI Scheduler project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- OpenAI for providing the GPT model used in task planning
- Notion for their API
- Google for the Calendar API
