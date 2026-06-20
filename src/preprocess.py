import pandas as pd
import numpy as np

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def load_data(path):
    return pd.read_csv(path)


def _parse_datetime(series):
    return pd.to_datetime(series, errors="coerce", utc=True).dt.tz_convert(None)


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["start_datetime", "end_datetime", "created_date", "resolved_datetime", "closed_datetime", "modified_datetime"]:
        if col in df.columns:
            df[col] = _parse_datetime(df[col])

    df["latitude"] = pd.to_numeric(df.get("latitude"), errors="coerce")
    df["longitude"] = pd.to_numeric(df.get("longitude"), errors="coerce")
    df = df[(df["latitude"].between(-90, 90)) & (df["longitude"].between(-180, 180))]
    df = df[(df["latitude"] != 0) & (df["longitude"] != 0)]

    df["requires_road_closure"] = df.get("requires_road_closure", False).fillna(False).astype(str).str.lower().isin(["true", "1", "yes"])
    df["priority"] = df.get("priority", "Medium").fillna("Medium")
    df["priority_score"] = df["priority"].astype(str).str.lower().map(PRIORITY_MAP).fillna(2)

    start = df.get("start_datetime")
    end = df.get("resolved_datetime")
    if end is None:
        end = df.get("end_datetime")
    else:
        end = end.fillna(df.get("end_datetime"))
    duration = (end - start).dt.total_seconds() / 3600
    df["duration_hours"] = duration.clip(lower=0, upper=24).fillna(duration.median() if duration.notna().any() else 1)
    df["duration_hours"] = df["duration_hours"].replace([np.inf, -np.inf], np.nan).fillna(1)

    df["hour"] = df["start_datetime"].dt.hour.fillna(12).astype(int)
    df["dayofweek"] = df["start_datetime"].dt.dayofweek.fillna(0).astype(int)
    df["month"] = df["start_datetime"].dt.month.fillna(1).astype(int)
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
    df["is_peak_hour"] = df["hour"].isin([8, 9, 10, 17, 18, 19, 20]).astype(int)

    text_cols = ["event_type", "event_cause", "corridor", "zone", "junction", "police_station", "veh_type", "status"]
    for c in text_cols:
        if c not in df.columns:
            df[c] = "unknown"
        df[c] = df[c].fillna("unknown").astype(str).str.strip().replace("", "unknown")

    df["event_is_planned"] = (df["event_type"].str.lower() == "planned").astype(int)
    return df.reset_index(drop=True)


def build_target(df: pd.DataFrame) -> pd.Series:
    # Proxy congestion impact score because raw traffic volume/speed is absent.
    cause_risk = df["event_cause"].astype(str).str.lower().map({
        "protest": 92, "public_event": 86, "procession": 84, "vip_movement": 78,
        "construction": 70, "accident": 74, "vehicle_breakdown": 58,
    }).fillna(55)
    score = (
        cause_risk
        + df["priority_score"] * 7
        + df["requires_road_closure"].astype(int) * 18
        + df["is_peak_hour"] * 10
        + df["duration_hours"].clip(0, 8) * 2.5
        + df["event_is_planned"] * 4
    )
    return score.clip(0, 100).round(2)
