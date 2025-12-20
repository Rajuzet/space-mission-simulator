def safety_check(mission: dict):
    """
    Safety controller enforces no-go rules.
    """
    if mission["duration_days"] <= 0:
        return False, "Invalid mission duration"

    if mission["orbit"] == "GEO" and mission["duration_days"] > 180:
        return False, "GEO missions limited to 180 days"

    return True, "Safety checks passed"
  
