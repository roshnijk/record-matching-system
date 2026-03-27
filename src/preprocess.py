import pandas as pd

def load_and_clean_data():
    crm = pd.read_json("data/crm_events.json")
    cal = pd.read_json("data/calendar_events.json")

    # Fix malformed dates
    crm['meeting_date'] = crm['meeting_date'].astype(str)\
        .str.replace(r'[^0-9\-]', '', regex=True)\
        .str.strip()

    # Handle missing time correctly
    crm['meeting_time'] = crm['meeting_time'].fillna("00:00").astype(str)

    # Combine safely
    crm['datetime'] = pd.to_datetime(
        crm['meeting_date'] + " " + crm['meeting_time'],
        errors='coerce'
    )

    # Calendar datetime
    cal['datetime'] = pd.to_datetime(cal['start_time'], errors='coerce')

    # Normalize text
    for col in ['subject', 'client_name', 'client_company', 'location']:
        if col in crm.columns:
            crm[col] = crm[col].astype(str).str.lower()

    for col in ['title', 'location']:
        if col in cal.columns:
            cal[col] = cal[col].astype(str).str.lower()

    return crm, cal
