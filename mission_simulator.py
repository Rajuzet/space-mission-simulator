from agents.planner_agent import plan_mission
from agents.validator_agent import validate_plan
from agents.safety_controller import safety_check


def simulate_mission(mission: dict):
    """
    Orchestrates autonomous mission agents.
    """

    # Safety first
    safe, safety_msg = safety_check(mission)
    if not safe:
        return {
            "mission_name": mission["name"],
            "status": "ABORTED",
            "reason": safety_msg
        }

    # Planning
    plan = plan_mission(mission)

    # Validation
    valid, validation_msg = validate_plan(plan)
    if not valid:
        return {
            "mission_name": mission["name"],
            "status": "REJECTED",
            "reason": validation_msg
        }

    # Final decision
    return {
        "mission_name": mission["name"],
        "orbit": mission["orbit"],
        "status": "APPROVED",
        "decision": "PROCEED",
        "plan": plan,
        "notes": "Mission approved by autonomous agent pipeline"
    }
