from events.models import Event

class CalendarService:
  def __init__(self,event_repository):
    self.event_repo = event_repository
  def add_event(self,utitle,udate,utime):
    new_event = Event(None,utitle,udate,utime)
    new_id = self.event_repo.add(new_event)
    return new_id
  def get_by_id(self,id_chosen):
    return self.event_repo.get_event_by_id(id_chosen)
  def get_by_date(self,date):
    return self.event_repo.get_events_by_date(date)
  def delete_event(self,event_id):
    return self.event_repo.delete_event(event_id)
  def list_events(self):
    return self.event_repo.get_all()
