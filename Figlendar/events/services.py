from events.models import Event
from events.exceptions import EventNotFound
from events.schemas import EventUpdate
class CalendarService:
  def __init__(self,event_repository):
    self.event_repo = event_repository

  def add_event(self,utitle,udate,utime):
    new_event = Event(None,utitle,udate,utime)
    new_id = self.event_repo.add(new_event)
    return new_id
  
  def list_events(self):
    return self.event_repo.get_all()
  
  def get_by_id(self,id_chosen):
    return self.event_repo.get_event_by_id(id_chosen)
  
  def get_by_date(self,date):
    return self.event_repo.get_events_by_date(date)
  
  def update_event(self,event_id,event_update:EventUpdate):
    event = self.event_repo.get_event_by_id(event_id)
    if not event:
      raise EventNotFound(f"Event with id {event_id} no found")
    if event_update.title is not None:
      event.title = event_update.title
    if event_update.date is not None:
      event.date = event_update.date
    if event_update.time is not None:
      event.time = event_update.time
    updated_event = self.event_repo.update_event(event)
    return updated_event
  
  def delete_event(self,event_id):
    event = self.event_repo.delete_event(event_id)
    if not event:
      raise EventNotFound(f"Event with id {event_id} no found")
    return self.event_repo.delete_event(event_id)