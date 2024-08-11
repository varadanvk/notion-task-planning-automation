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
     ```

4. Set up Google Calendar API:
   - Follow the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python) to enable the API and download your `credentials.json` file
   - Place the `credentials.json` file in the project root

## Usage

1. Update the `database_id` in `main.py` with your Notion database ID.

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

## Future Development Plan

### 1. Cloud Hosting

#### 1.1 Set up cloud infrastructure

- [ ] Choose a cloud provider (e.g., AWS, Google Cloud, or Azure)
- [ ] Set up a virtual machine or serverless environment
- [ ] Configure necessary security groups and access controls

#### 1.2 Implement efficient update mechanism

- [] Develop a method to track the last processed task
  - [ ] Store last processed task ID in a database or file
  - [ ] Implement comparison logic to identify new tasks
- [ ] Modify main script to only process new or updated tasks
  - [ ] Update Notion API queries to filter for new/updated tasks
  - [ ] Implement differential update logic in the planner

#### 1.3 Implement selective scheduling

- [ ] Modify the planner to handle individual task scheduling
  - [ ] Update `create_calendar_events` method to accept a single task
  - [ ] Implement logic to merge new event with existing schedule

#### 1.4 Set up automated running

- [ ] Implement a cron job or scheduled task to run the script periodically
- [ ] Set up logging to track script executions and any errors

### 2. Improve AI Responses

#### 2.1 Enhance conflict avoidance

- [ ] Modify the prompt to emphasize the importance of avoiding conflicts
- [ ] Implement a post-processing step to double-check for conflicts
  - [ ] Develop a function to detect overlaps between events
  - [ ] Implement a resolution strategy for any detected conflicts

#### 2.2 Ensure future scheduling

- [ ] Add a pre-processing step to filter out past dates
- [ ] Modify the prompt to explicitly require future dates
- [ ] Implement a post-processing step to verify all generated events are in the future

#### 2.3 Optimize time slot selection

- [ ] Analyze user's typical schedule to identify preferred time slots
- [ ] Modify the prompt to include preferred time slots for different task types
- [ ] Implement a scoring system for generated schedules to optimize task placement

### 3. Develop Frontend

#### 3.1 Design user interface

- [ ] Create wireframes for key pages (dashboard, task list, calendar view)
- [ ] Design a cohesive visual style and color scheme

#### 3.2 Implement frontend framework

- [ ] Choose a frontend framework (e.g., React, Vue.js, or Angular)
- [ ] Set up the project structure and build pipeline
- [ ] Implement responsive design for mobile and desktop views

#### 3.3 Develop key components

- [ ] Create a dashboard component to display upcoming tasks and events
- [ ] Implement a task list component with filtering and sorting capabilities
- [ ] Develop a calendar view component to visualize scheduled tasks and events

#### 3.4 Integrate with backend

- [ ] Implement API calls to fetch data from the backend
- [ ] Develop real-time updates using WebSockets or polling
- [ ] Implement error handling and loading states

#### 3.5 Implement user authentication

- [ ] Set up user registration and login system
- [ ] Implement OAuth for Notion and Google Calendar
- [ ] Develop user profile management features

### 4. Testing and Quality Assurance

#### 4.1 Develop automated tests

- [ ] Write unit tests for critical functions in each module
- [ ] Implement integration tests for the entire scheduling pipeline
- [ ] Develop end-to-end tests for the frontend

#### 4.2 Perform manual testing

- [ ] Create a test plan covering various use cases
- [ ] Conduct usability testing with a small group of users
- [ ] Document and address any identified issues or user feedback

### 5. Documentation and Deployment

#### 5.1 Update documentation

- [ ] Revise the README with new features and setup instructions
- [ ] Create user documentation explaining how to use the system
- [ ] Develop API documentation for backend endpoints

#### 5.2 Prepare for deployment

- [ ] Set up a staging environment for final testing
- [ ] Develop a deployment script for easy updates
- [ ] Create a rollback plan in case of deployment issues

#### 5.3 Launch and monitor

- [ ] Deploy the application to the production environment
- [ ] Set up monitoring and alerting for critical system components
- [ ] Develop a plan for ongoing maintenance and updates

## Contributing

Contributions to the AI Scheduler project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

We welcome contributions to help achieve the goals outlined in our development plan. If you're interested in working on any of these tasks, please check our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to get started.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- OpenAI for providing the GPT model used in task planning
- Notion for their API
- Google for the Calendar API
