def categorize_tii(score: float) -> str:
    if score < 31:
        return "Low"
    if score < 61:
        return "Medium"
    if score < 81:
        return "High"
    return "Critical"


def traffic_impact_index(severity, duration_hours, priority_score, road_closure, road_capacity=100):
    closure_factor = 1.35 if road_closure else 1.0
    capacity = max(float(road_capacity), 1.0)
    raw = (float(severity) * (1 + float(duration_hours) / 8) * (1 + float(priority_score) / 5) * closure_factor) / (capacity / 100)
    return max(0, min(100, round(raw, 2)))
