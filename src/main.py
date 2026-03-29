import pandas as pd
from preprocess import load_and_clean_data
from matcher import compute_score
from evaluate import evaluate


crm, cal = load_and_clean_data()
print(crm.columns)
print(cal.columns)
results = []

for _, c in crm.iterrows():
    for _, k in cal.iterrows():

        if pd.isna(c['datetime']) or pd.isna(k['datetime']):
            continue

        # Blocking (2-hour window)
        if abs((c['datetime'] - k['datetime']).total_seconds()) > 7200:
            continue

        score = compute_score(c, k)

        results.append({
            "crm_id": c['crm_id'],
            "cal_id": k['event_id'],
            "score": score,
            "match": score > 0.5
        })

df = pd.DataFrame(results, columns=["crm_id", "cal_id", "score", "match"])
df.to_csv("output/predictions.csv", index=False)
#testing
print("DF COLUMNS:", df.columns)
print("DF SHAPE:", df.shape)
print(df.head())

evaluate(df)
