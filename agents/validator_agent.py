def validate_plan(plan: dict):
    """
    Validator agent checks if the plan is feasible.
    """
    if plan["estimated_duration"] > 365:
        return False, "Duration exceeds safe limits"

    if plan["target_orbit"] not in ["LEO", "GEO", "MEO"]:
        return False, "Unsupported orbit type"

    return True, "Plan validated"
