<<<<<<< HEAD
from events.models import Event,SQLEvent
=======
from models import Event,SQLEvent
>>>>>>> 06e0675f031124a484bfee8a756d804cb93926aa

class SqliteEventRepository:
  def __init__(self,session):
    self.session = session
  
  def add(self,event):
    sql_event = SQLEvent(title=event.title,date=event.date,time=event.time)
    self.session.add(sql_event)
    self.session.commit()
    return sql_event.id
  
  def get_all(self):
    sql_events = self.session.query(SQLEvent).all()
    results = []
    for sqlevent in sql_events:
      results.append(Event(sqlevent.id,sqlevent.title,sqlevent.date,sqlevent.time))
    return results
<<<<<<< HEAD
  
  def get_event_by_id(self,event_id):
    return self.session.query(SQLEvent).filter_by(id=event_id).first()
  
=======
  def get_event_by_id(self,event_id):
    return self.session.query(SQLEvent).filter_by(id=event_id).first()
>>>>>>> 06e0675f031124a484bfee8a756d804cb93926aa
  def get_events_by_date(self,date):
    sql_events = self.session.query(SQLEvent).filter(SQLEvent.date == date).all()
    results = []
    for event in sql_events:
      new_event = Event(event.id,event.title,event.date,event.time)
      results.append(new_event)
    return results
<<<<<<< HEAD
  
  def update_event(self,event:Event):
    sql_event = self.session.query(SQLEvent).filter_by(id=event.id).first()
    if sql_event:
      if event.title is not None:
        sql_event.title = event.title
      if event.date is not None:
        sql_event.date = event.date
      if event.time is not None:
        sql_event.time = event.time
      self.session.commit()
      return sql_event
    return None
=======
>>>>>>> 06e0675f031124a484bfee8a756d804cb93926aa
  def delete_event(self,event_id):
    event = self.get_event_by_id(event_id)
    if event:
      self.session.delete(event)
      self.session.commit()
      return True
    else:
<<<<<<< HEAD
      return False
=======
      return False
class ListEventRepository:

  def __init__(self):
    self._events = []
    self._next_id:int = 1
    
  def add(self,event):
    event.id = self._next_id
    self._next_id += 1
    self._events.append(event)
    return event.id

  def get_all(self):
    return list(self._events)

  def get_by_id(self,id_chosen):
    for event in self._events:
      if event.id == id_chosen:
        return event
    return None

  def get_events_by_date(self,date):
    results = []
    for event in self._events:
      if event.date == date:
        results.append(event)
    return results
  
  def delete(self, event_id):
    for index,event in enumerate(self._events):
      if event.id == event_id:
        self._events.pop(index)
        return True
    return False 
>>>>>>> 06e0675f031124a484bfee8a756d804cb93926aa
