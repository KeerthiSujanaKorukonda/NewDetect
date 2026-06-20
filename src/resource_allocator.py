def recommend_resources(congestion_score, requires_road_closure=False, event_type="unplanned"):
    score = float(congestion_score)
    planned_boost = 1 if str(event_type).lower() == "planned" else 0
    if score >= 85:
        base = dict(police=22, barricades=18, diversion_routes=4, tow_trucks=3, ambulances=2, control_room_staff=4)
    elif score >= 70:
        base = dict(police=15, barricades=12, diversion_routes=3, tow_trucks=2, ambulances=1, control_room_staff=3)
    elif score >= 50:
        base = dict(police=8, barricades=6, diversion_routes=2, tow_trucks=1, ambulances=1, control_room_staff=2)
    else:
        base = dict(police=4, barricades=2, diversion_routes=1, tow_trucks=0, ambulances=0, control_room_staff=1)
    if requires_road_closure:
        base["police"] += 4
        base["barricades"] += 6
        base["diversion_routes"] += 1
    if planned_boost:
        base["control_room_staff"] += 1
    return base
