# EventIQ: Event-Driven Congestion Forecasting

EventIQ predicts event-related traffic impact and recommends manpower, barricading, emergency support, and diversion plans.


## Dashboard

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bbf4d3bf-7fdc-4160-9183-026f3ee8aadb" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a84c472d-a90f-4566-bdd1-c776cd3b7f8f" />

## Architecture

<img width="1536" height="1023" alt="image" src="https://github.com/user-attachments/assets/fe2f5a74-6f5b-41c5-aca5-ebe2282f2e02" />


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
