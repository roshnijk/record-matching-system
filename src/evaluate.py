import json
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate(predictions_df):
    labels = json.load(open("data/evaluation_labels.json"))

    y_true = []
    y_pred = []

    for pair in labels["cross_source_pairs"]:
        crm_id = pair["crm_id"]
        cal_id = pair["calendar_id"]
        actual = pair["match"]

        pred = predictions_df[
            (predictions_df["crm_id"] == crm_id) &
            (predictions_df["cal_id"] == cal_id)
        ]

        if len(pred) == 0:
            predicted = 0
        else:
            predicted = int(pred.iloc[0]["match"])

        y_true.append(actual)
        y_pred.append(predicted)

    print("Precision:", precision_score(y_true, y_pred))
    print("Recall:", recall_score(y_true, y_pred))
    print("F1 Score:", f1_score(y_true, y_pred))
