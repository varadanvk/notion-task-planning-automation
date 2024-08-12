from services.calendar import CalendarService

calendar = CalendarService()

events = calendar.get_events()
print(events)