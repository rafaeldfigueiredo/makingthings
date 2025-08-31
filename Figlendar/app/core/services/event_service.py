from app.core.entities.event import Event


class EventService:
    def __init__(self):
        self._events = []
        self._next_id = 1

    def create_event(self, event: Event):
        new_event = {
            "id": self._next_id,
            "title": event.title,
            "description": event.description,
            "startTime": event.startTime,
            "endTime": event.endTime
        }
        self._events.append(new_event)
        self._next_id += 1
        return new_event

    def list_events(self):
        return self._events
