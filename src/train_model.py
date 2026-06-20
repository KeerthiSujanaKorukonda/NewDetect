import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from config import DATA_PATH, MODEL_PATH, FEATURES_PATH
from preprocess import load_data, clean_events, build_target
from feature_engineering import make_features


def train():
    df = clean_events(load_data(DATA_PATH))
    y = build_target(df)
    X = make_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=250, max_depth=18, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Rows: {len(df)} | Features: {X.shape[1]}")
    print(f"MAE: {mean_absolute_error(y_test, pred):.3f}")
    print(f"R2 : {r2_score(y_test, pred):.3f}")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(list(X.columns), FEATURES_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    train()
