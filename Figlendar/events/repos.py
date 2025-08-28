from events.models import Event,SQLEvent

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
  
  def get_event_by_id(self,event_id):
    return self.session.query(SQLEvent).filter_by(id=event_id).first()
  
  def get_events_by_date(self,date):
    sql_events = self.session.query(SQLEvent).filter(SQLEvent.date == date).all()
    results = []
    for event in sql_events:
      new_event = Event(event.id,event.title,event.date,event.time)
      results.append(new_event)
    return results
  
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
  def delete_event(self,event_id):
    event = self.get_event_by_id(event_id)
    if event:
      self.session.delete(event)
      self.session.commit()
      return True
    else:
      return False