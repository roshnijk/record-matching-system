
from fastapi import FastAPI
from matcher import compute_score

app = FastAPI()

@app.post("/match")
def match_records(record_a: dict, record_b: dict):
    score = compute_score(record_a, record_b)
    return {
        "match": score > 0.7,
        "score": score
    }
