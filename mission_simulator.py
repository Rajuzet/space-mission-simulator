def analyze_mission(mission):
    """
    Analyze mission parameters and assign risk.
    """
    if mission["orbit"] == "LEO":
        return "LOW", 0.9
    elif mission["orbit"] == "GEO":
        return "MEDIUM", 0.75
    else:
        return "HIGH", 0.6


def decide_action(risk_level):
    """
    Decide whether mission should proceed.
    """
    if risk_level == "HIGH":
        return "HOLD"
    return "PROCEED"


def simulate_mission(mission: dict):
    """
    Main autonomous mission simulation entry point.
    """
    risk_level, confidence = analyze_mission(mission)
    decision = decide_action(risk_level)

    return {
        "mission_name": mission["name"],
        "orbit": mission["orbit"],
        "status": "SIMULATED",
        "decision": decision,
        "risk_level": risk_level,
        "confidence": confidence,
        "notes": "Autonomous decision generated via modular logic"
    }
    
