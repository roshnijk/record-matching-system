from rapidfuzz import fuzz
import pandas as pd

def text_similarity(a, b):
    if pd.isna(a) or pd.isna(b):
        return 0
    return fuzz.token_sort_ratio(str(a), str(b)) / 100

def time_similarity(t1, t2):
    if pd.isna(t1) or pd.isna(t2):
        return 0
    diff = abs((t1 - t2).total_seconds()) / 60
    return max(0, 1 - diff / 120)

def compute_score(crm, cal):
    company_match = text_similarity(crm['client_company'], cal['title'])
    person_match = text_similarity(crm['client_name'], " ".join(cal['attendees']))
    title_sim = text_similarity(crm['subject'], cal['title'])
    location_sim = text_similarity(crm['location'], cal['location'])
    time_sim = time_similarity(crm['datetime'], cal['datetime'])

    score = (
        0.35 * company_match +
        0.25 * person_match +
        0.15 * title_sim +
        0.15 * time_sim +
        0.10 * location_sim
    )

    # Custom tweak (to stand out)
    if "internal" in str(crm.get('meeting_type', '')).lower():
        score *= 0.8

    return score
