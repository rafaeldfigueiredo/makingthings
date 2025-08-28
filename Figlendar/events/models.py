from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SQLEvent(Base):
    __tablename__ = 'events'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    date = Column(String)
    time = Column(String)

class Event:
    def __init__(self,id,title,date,time):
      self.id = id
      self.title = title
      self.date = date
      self.time = time