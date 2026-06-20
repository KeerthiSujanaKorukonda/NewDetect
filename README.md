# EventIQ: Event-Driven Congestion Forecasting

EventIQ predicts event-related traffic impact and recommends manpower, barricading, emergency support, and diversion plans.

## What it uses
- Historical Astram event data
- Planned/unplanned event type
- Event cause
- Location
- Time and duration
- Priority
- Road closure requirement

## Setup
```bash
cd EventIQ
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

## Train model
```bash
python src/train_model.py
```

## Test prediction
```bash
python src/predict.py
```

## Run dashboard
```bash
streamlit run dashboard/app.py
```

## Run API
```bash
uvicorn api.main:app --reload
```
Open `/docs` in the browser to test the API.

## Core outputs
- Congestion score: 0 to 100
- Traffic Impact Index
- Risk category: Low / Medium / High / Critical
- Police, barricades, ambulances, tow trucks, control-room staff
- Primary and backup diversion suggestions

## Note
The uploaded dataset does not contain real traffic speeds or vehicle counts, so this project creates a practical proxy target for congestion impact using event severity, priority, duration, peak hour, and closure requirement. If live traffic speed/volume data is added later, replace `build_target()` in `src/preprocess.py` with the real observed delay or congestion label.
