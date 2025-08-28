from events.exceptions import EventNotFound
from events.repos import SqliteEventRepository
from events.database import db_session
from events.services import CalendarService

event_repo = SqliteEventRepository(db_session)
my_calendar = CalendarService(event_repo)

def menu():
  print("\nWelcome to Figlendar")
  while True:
    choice = input("\n1) Create New Event\n2) List All Events\n3) List One Event\n4) List Events by Date\n5) Delete Event\n6) Exit\nR: ")
    match(choice):
      case '1': #Create New Event
        utitle = input("Title of the Event:\nR: ");udate = input("Date of the Event:\nR: ");utime = input("Time of the Event:\nR: ")
        my_calendar.add_event(utitle,udate,utime)
      case '2': # List All Events
        events = my_calendar.list_events()
        if events:
          for event in events:
            print(f"[{event.id}] {event.title} at {event.date} - {event.time}")
        else:
          print("No events!")
      case '3': # Select one event
        choice = int(input("\nSelect the event by id (case-sensitive)\nR:"))
        event = my_calendar.get_by_id(choice)
        if event:
          print(f"[{event.id}] {event.title} at {event.date} - {event.time}")
        else:
          print("\nNo event found!")
        
      case '4': # Select events by date
        choice = input("\nSelect the events by date\nR: ")
        events = my_calendar.get_by_date(choice)
        if events:
          for event in events:
            print(f"[{event.id}] {event.title} at {event.date} - {event.time}")
        else:
          print("\nNo events!")
      case '5': # Delete event
        choice = int(input("\nSelect the event by id (case-sensitive)\nR:"))
        
        try:
          my_calendar.delete_event(choice)
          print("Event deleted.")
        except EventNotFound as error:
          print(f"Something went wrong: {error}")
      case '6': # Exit
        print("\nBye!")
        break
      case _: # Invalid Option
        print("\nWrong Option!")
        

if __name__ == "__main__":
  menu()