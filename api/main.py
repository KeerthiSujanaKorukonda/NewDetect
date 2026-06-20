import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_event

app = FastAPI(title="EventIQ API")

class EventRequest(BaseModel):
    event_type: str = "planned"
    event_cause: str = "public_event"
    latitude: float = 12.9716
    longitude: float = 77.5946
    requires_road_closure: bool = False
    start_datetime: str = "2026-06-20 17:00:00"
    end_datetime: str = "2026-06-20 21:00:00"
    priority: str = "High"
    corridor: str = "unknown"
    zone: str = "unknown"
    junction: str = "unknown"
    police_station: str = "unknown"
    veh_type: str = "unknown"
    status: str = "open"

@app.get("/")
def root():
    return {"message": "EventIQ API running"}

@app.post("/predict")
def predict(req: EventRequest):
    return predict_event(req.model_dump())
