def plan_mission(mission: dict):
    """
    Planner agent creates a high-level mission plan.
    """
    plan = {
        "target_orbit": mission["orbit"],
        "estimated_duration": mission["duration_days"],
        "payload_status": "READY"
    }
    return plan
  
