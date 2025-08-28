from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from events.exceptions import EventNotFound
from events.services import CalendarService
from events.repos import SqliteEventRepository
from events.database import db_session
from events.schemas import EventCreate, EventUpdate

event_repo = SqliteEventRepository(db_session)
calendar_service = CalendarService(event_repo)

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do seu calendário!"}

@app.get("/events/")
def list_events():
    # A magia acontece aqui: o servico lida com a logica de negocio
    return calendar_service.list_events()

@app.post("/events/")
def create_event(event:EventCreate):
    event_id = calendar_service.add_event(
        utitle=event.title,
        udate=event.date,
        utime=event.time
    )
    return {"message":f"Event created","EventID":event_id}

@app.put("/events/{event_id}")
def update_event(event_id:int,event_to_update:EventUpdate):
    try:
        updated_event = calendar_service.update_event(event_id,event_to_update)
        return {"message":"Event deleted succesfully","event":updated_event}
    except EventNotFound as error:
        raise HTTPException(status_code=404,detail=str(error))    


@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    try:
        calendar_service.delete_event(event_id)
        return {"message":"Event deleted succesfully"}
    except EventNotFound as error:
        raise HTTPException(status_code=404,detail=str(error))
