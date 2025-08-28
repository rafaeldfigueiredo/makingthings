from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///my_calendar.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()