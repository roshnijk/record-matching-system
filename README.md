# Record Matching System

## Overview

The goal of this task was to match records from two different systems (CRM and calendar) that refer to the same real-world meeting, even though there is no shared identifier between them.

Instead of directly jumping into a machine learning model, I treated this as a similarity-based matching problem, mainly because the dataset is small and the labels provided are only partial.

---

## How I approached the problem

I broke the problem into three main steps:

1. Cleaning and standardizing the data
2. Reducing the number of comparisons (blocking)
3. Scoring how similar two records are

The idea was to create a simple but explainable system that can be improved later if needed.

---

## Data observations and challenges

While exploring the data, I noticed a few practical issues:

* Date formats were not consistent (some malformed values)
* Some records had missing fields (like location or attendees)
* Calendar timestamps had timezone differences
* Same meeting sometimes had slightly different descriptions across systems
* There are overlapping or near-duplicate meetings (especially in calendar data)
* Labels are incomplete, so not all true matches are known

Because of this, I focused more on making the system tolerant to noise rather than trying to make it perfect.

---

## Matching logic

For each CRM–calendar pair, I compute a similarity score using a few signals:

* Client/company name
* Participant names (from attendees)
* Title/subject similarity
* Time difference between meetings
* Location similarity

Not all features are equally reliable, so I used a weighted combination:

* Company → strongest signal
* Participant → strong signal
* Title and time → moderate
* Location → weaker (can be noisy)

I used a threshold of 0.7 to decide whether two records match.

I also slightly reduced the score for internal meetings, since they tend to have weaker identifying information compared to client meetings.

---

## Reducing comparisons (blocking)

Instead of comparing every record with every other record, I filtered candidate pairs based on time.

Only meetings within a 2-hour window are compared.
This helps reduce noise and keeps the matching more realistic.

---

## Evaluation

I evaluated the system using the provided labeled pairs.

Metrics used:

* Precision
* Recall
* F1 score

One important thing to note is that the labels are partial, so recall is likely underestimated — there could be correct matches that are simply not labeled.

---

## Key decisions and trade-offs

* I chose a heuristic approach instead of training a model due to limited labeled data
* Time-based filtering improves performance but may miss some edge cases
* Fuzzy matching helps catch variations in text but can sometimes match unrelated records
* The threshold was chosen to balance false positives and false negatives

---

## Where the system struggles

Some cases are still tricky:

* Multiple meetings with the same participants on the same day
* Recurring meetings vs one-off CRM entries
* Missing client or attendee information
* Very similar meeting titles across different clients

---

## What I would improve with more time

* Learn weights using a simple model (e.g., logistic regression)
* Use embeddings for better text similarity
* Improve blocking (for example using approximate nearest neighbors)
* Add feedback loop if user corrections are available

---

## AI usage

I used AI tools to speed up brainstorming and structure the solution, especially for feature ideas and API scaffolding.

However, the final approach, feature selection, scoring logic, and trade-offs were manually reviewed and adjusted based on the data.

---

## How to run

```bash
pip install -r requirements.txt
python src/main.py
```

To run the API:

```bash
uvicorn src.api:app --reload
```

---

## Time spent

Approximately 3–4 hours

