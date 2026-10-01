# Loads the trained machine learning model and provides career prediction functions.

import json
import joblib
import pandas as pd

from data.skills import SKILL_LIST

# Load the trained model pipeline (StandardScaler + LogisticRegression) from disk.
saved = joblib.load("data/model.pkl")
pipeline = saved["pipeline"]

# Load the jobs data from the JSON file.
with open("data/jobs.json", "r", encoding="utf-8") as f:
    jobs_list = json.load(f)

# Build a lookup dictionary mapping job IDs to job objects for quick access.
jobs_by_id = {}
for job in jobs_list:
    jobs_by_id[job["id"]] = job


def get_top5_jobs(skill_scores):
    # Predict the top 5 most suitable careers based on the user's skill scores.
    # skill_scores is a dict like {"analytical_thinking": 7, "creativity": 3, ...}

    # Build a DataFrame row with the user's skill scores.
    row = {}
    for skill in SKILL_LIST:
        row[skill] = [skill_scores[skill]]
    X = pd.DataFrame(row)

    # Get prediction probabilities for all career classes.
    probabilities = pipeline.predict_proba(X)[0]
    job_ids = pipeline.classes_

    # Pair job IDs with their probabilities and sort descending by probability.
    pairs = list(zip(job_ids, probabilities))
    pairs.sort(key=lambda pair: pair[1], reverse=True)

    # Build the top 5 results list.
    top5 = []
    for job_id, prob in pairs[:5]:
        top5.append({
            "job": jobs_by_id[job_id],
            "probability": float(prob),  # Match score from the model.
        })

    return top5


def get_best_job(skill_scores):
    # Return only the single best matching career.
    top5 = get_top5_jobs(skill_scores)
    return top5[0]


def explain_match(skill_scores, job):
    # Generate a simple explanation of why this career matches the user.
    # Compares the user's strongest relevant skills against the career's required skills.
    # This is for display purposes only and does not affect ranking.

    # Get the career's required skills list, or fall back to all skills if none specified.
    required = job.get("required_skills", [])
    if not required:
        required = SKILL_LIST

    # Rank the user's skills that are relevant to this career, strongest first.
    relevant_scores = [(skill, skill_scores[skill]) for skill in required]
    relevant_scores.sort(key=lambda pair: pair[1], reverse=True)

    # Select the top relevant skills where the user scored at least 5.0.
    top_reasons = [skill for skill, score in relevant_scores[:4] if score >= 5.0]
    if not top_reasons:
        # If the user is weak in all required skills, show the top two anyway.
        top_reasons = [skill for skill, _ in relevant_scores[:2]]

    return top_reasons


def required_skills_compatibility(skill_scores, job):
    # Calculate a compatibility score based on the career's expected skill levels.
    # Checks how close the user's scores are to what the career expects (skills_mean).
    # This is an explanatory layer only and never overrides the ML ranking.

    # Get the career's required skills list.
    required = job.get("required_skills", [])
    if not required:
        return 1.0  # If no required skills, return perfect compatibility.

    skills_mean = job["skills_mean"]
    hits = 0
    # Count how many required skills the user is within 2 points of the expected value.
    for skill in required:
        expected = skills_mean[skill]
        user_value = skill_scores[skill]
        if user_value >= expected - 2:
            hits += 1

    # Return the proportion of required skills that the user meets.
    return round(hits / len(required), 2)


# Quick test to verify the module works correctly.
if __name__ == "__main__":
    from scoring import personality_to_skills

    # Test with a fixed set of answers.
    test_answers = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    scores = personality_to_skills(test_answers)
    print("skill scores:", scores)

    best = get_best_job(scores)
    print("best job:", best["job"]["title"]["en"], "-", round(best["probability"] * 100, 1), "%")

    print("\ntop 5:")
    for item in get_top5_jobs(scores):
        reasons = explain_match(scores, item["job"])
        compat = required_skills_compatibility(scores, item["job"])
        print(item["job"]["title"]["en"], "-", round(item["probability"] * 100, 1), "%",
              "| reasons:", reasons, "| required_skills_compat:", compat)