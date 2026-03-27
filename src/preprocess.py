import pandas as pd

def load_and_clean_data():
    crm = pd.read_json("data/crm_events.json")
    cal = pd.read_json("data/calendar_events.json")

    # Fix malformed dates
    crm['meeting_date'] = crm['meeting_date'].astype(str).str.replace(r'[^0-9\-]', '', regex=True)

    # Fill missing time
    crm['meeting_time'] = crm['meeting_time'].fillna("00:00")

    # Convert datetime

    crm['meeting_date'] = pd.to_datetime(crm['meeting_date'], errors='coerce')

    crm['datetime'] = crm['meeting_date'] + pd.to_timedelta(
    crm['meeting_time'].fillna("00:00") + ":00"
    )

    cal['datetime'] = pd.to_datetime(cal['start_time'], errors='coerce')

    # Normalize text
    for col in ['subject', 'client_name', 'client_company', 'location']:
        crm[col] = crm[col].astype(str).str.lower()

    for col in ['title', 'location']:
        cal[col] = cal[col].astype(str).str.lower()

    return crm, cal
