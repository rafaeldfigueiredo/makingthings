from app.api.calendar_routes import router as calendar_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(calendar_router)

@app.get("/ping")
async def read_root():
  return {"message":"pong"}