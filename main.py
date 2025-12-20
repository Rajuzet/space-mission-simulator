from fastapi import FastAPI
from pydantic import BaseModel
from mission_simulator import simulate_mission

app = FastAPI(title="Space Mission Simulator")


class MissionInput(BaseModel):
    name: str
    orbit: str        # LEO, GEO, MEO
    duration_days: int


@app.get("/")
def root():
    return {"message": "Space Mission Simulator API is running"}


@app.post("/simulate-mission")
def simulate(mission: MissionInput):
    return simulate_mission(mission.dict())
