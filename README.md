# Record Matching System

## Overview

This project focuses on matching meeting records coming from two different systems — a CRM and a calendar — where there is no shared identifier between them.

The goal is to identify which records refer to the same real-world meeting, despite inconsistencies in format, missing values, and partial labeling.

---

## Observations

During evaluation, I noticed that the system produced very few or no matches at higher thresholds.

This suggests that the current feature set and similarity scoring are not strong enough to confidently link records in many cases. Rather than forcing matches by aggressively lowering the threshold, I chose to keep the system conservative and use this as a signal for where improvements are needed.

This helped highlight the importance of stronger text similarity methods and better feature representation.


## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the matching pipeline:

```bash
python src/main.py
```

This will:

* Load and clean both datasets
* Generate match predictions
* Evaluate results using the provided labels
* Save predictions to `output/predictions.csv`

3. (Optional) Run the API:

```bash
uvicorn src.api:app --reload
```

---

## Approach

I approached this as a record linkage problem under noisy and partially labeled conditions.

Instead of directly using a machine learning model, I started with a heuristic-based approach. Given the small dataset and incomplete labels, this made it easier to reason about the results and debug issues.

The pipeline has three main parts:

### 1. Data Cleaning

* Standardized date and time fields into a unified datetime
* Handled malformed date values and missing fields
* Normalized text fields (lowercasing, basic cleaning)

This step was important because even small inconsistencies (like spacing or casing) were affecting similarity scores.

---

### 2. Candidate Selection (Blocking)

To avoid comparing every record with every other record, I limited comparisons to meetings that are close in time (within a fixed window).
This reduces unnecessary comparisons and makes the matching more realistic.

---

### 3. Similarity Scoring

For each candidate pair, I calculated a weighted similarity score based on:

* Client/company name
* Participants / attendees
* Meeting title / subject
* Time difference
* Location

Not all features are equally reliable, so I assigned higher weight to company and participants, and lower weight to location.
A threshold is used to decide whether two records match.

---

## Evaluation

I evaluated the system using the provided labeled pairs and measured:

* Precision
* Recall
* F1 Score

One important observation is that the labels are partial, so recall may be underestimated — there could be valid matches that are not labeled.
During testing, I also noticed cases where no matches were predicted at higher thresholds. This helped in tuning the threshold and understanding the trade-off between precision and recall.

---

## Key Decisions and Trade-offs

* **Heuristic vs ML**
  I chose a heuristic approach due to limited labeled data and the need for interpretability.

* **Threshold tuning**
  A higher threshold improves precision but can reduce recall significantly. I adjusted it based on observed results.

* **Feature weighting**
  Company and participant information were treated as stronger signals compared to title or location.

* **Handling noisy data**
  Instead of strict matching, I used flexible comparisons to tolerate inconsistencies in real-world data.

---

## Challenges Faced

* Inconsistent date formats and datatype issues while combining date and time
* Schema mismatches between source data and evaluation labels (especially ID fields)
* Some records missing key fields like attendees or location
* Difficulty in capturing similarity for semantically similar but differently worded titles

---

## What I Would Improve

With more time, I would:

* Train a simple model (e.g., logistic regression) on engineered features
* Use text embeddings for better semantic similarity
* Improve blocking strategy to handle edge cases more efficiently
* Add a feedback loop to refine matching over time

---
## AI Usage

I used AI tools mainly to speed up initial development, especially for structuring the pipeline and brainstorming possible features for matching.

However, I found that some of the generated code did not handle real-world data issues well. For example, there were datatype inconsistencies when combining date and time fields, and assumptions about column names did not always match the actual data. I had to debug and correct these parts manually.

I also adjusted the matching logic and thresholds based on observed outputs rather than relying on default suggestions.

Overall, AI helped accelerate the starting point, but significant refinement was needed to make the solution work reliably on the given dataset.


