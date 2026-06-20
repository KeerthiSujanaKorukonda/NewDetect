import pandas as pd

CATEGORICAL = ["event_type", "event_cause", "corridor", "zone", "junction", "police_station", "veh_type", "status"]
NUMERIC = ["latitude", "longitude", "duration_hours", "priority_score", "hour", "dayofweek", "month", "is_weekend", "is_peak_hour", "event_is_planned"]


def make_features(df: pd.DataFrame, fit_columns=None):
    X_num = df[NUMERIC].copy()
    X_cat = pd.get_dummies(df[CATEGORICAL], dummy_na=False)
    X = pd.concat([X_num, X_cat], axis=1)
    if fit_columns is not None:
        X = X.reindex(columns=fit_columns, fill_value=0)
    return X
