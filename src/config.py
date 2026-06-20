from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "events.csv"
MODEL_PATH = ROOT_DIR / "models" / "eventiq_model.joblib"
FEATURES_PATH = ROOT_DIR / "models" / "feature_columns.joblib"
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
