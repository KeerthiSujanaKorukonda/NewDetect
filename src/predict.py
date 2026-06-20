import joblib
import pandas as pd
from config import MODEL_PATH, FEATURES_PATH
from preprocess import clean_events
from feature_engineering import make_features
from traffic_index import traffic_impact_index, categorize_tii
from resource_allocator import recommend_resources
from diversion_engine import recommend_diversions


def predict_event(event: dict):
    model = joblib.load(MODEL_PATH)
    cols = joblib.load(FEATURES_PATH)
    df = clean_events(pd.DataFrame([event]))
    X = make_features(df, fit_columns=cols)
    congestion = round(float(model.predict(X)[0]), 2)
    row = df.iloc[0]
    tii = traffic_impact_index(congestion, row["duration_hours"], row["priority_score"], row["requires_road_closure"])
    return {
        "congestion_score": congestion,
        "traffic_impact_index": tii,
        "risk_category": categorize_tii(tii),
        "resources": recommend_resources(congestion, row["requires_road_closure"], row["event_type"]),
        "diversions": recommend_diversions(row["latitude"], row["longitude"], congestion),
    }

if __name__ == "__main__":
    sample = {
        "event_type": "planned", "event_cause": "public_event", "latitude": 12.9716, "longitude": 77.5946,
        "requires_road_closure": True, "start_datetime": "2026-06-20 17:00:00",
        "end_datetime": "2026-06-20 22:00:00", "priority": "High", "corridor": "CBD", "zone": "Central",
        "junction": "Main Junction", "police_station": "Central PS", "veh_type": "unknown", "status": "open"
    }
    print(predict_event(sample))
