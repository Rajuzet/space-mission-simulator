from fastapi import FastAPI
from mission_simulator import simulate_mission

app = FastAPI(title="Space Mission Simulator")

@app.get("/")
def root():
    return {"message": "Space Mission Simulator API is running"}

@app.post("/simulate-mission")
def simulate(mission_name: str):
    return simulate_mission(mission_name)
