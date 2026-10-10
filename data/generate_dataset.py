# Generates synthetic training data by sampling skill scores from normal distributions around each career's mean.

import json
import random
import pandas as pd

from data.skills import SKILL_LIST

# Number of samples to generate for each career.
SAMPLES_PER_JOB = 200
# Set random seed for reproducible results.
random.seed(42)


def load_jobs():
    # Load career profiles from the JSON file.
    with open("data/jobs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def make_samples_for_job(job):
    # Generate synthetic samples for a single career.
    rows = []
    mean_skills = job["skills_mean"]
    std = job["skills_std"]

    # Generate SAMPLES_PER_JOB samples for this career.
    for i in range(SAMPLES_PER_JOB):
        row = {}
        # Sample each skill from a normal distribution around the career's mean.
        for skill in SKILL_LIST:
            mean = mean_skills[skill]
            value = random.gauss(mean, std)

            # Clamp values to the 0-10 range.
            if value < 0:
                value = 0
            if value > 10:
                value = 10

            # Round to nearest integer for discrete skill scores.
            row[skill] = round(value)

        # Add the job ID as the target label.
        row["job_id"] = job["id"]
        rows.append(row)

    return rows


def main():
    # Main function to generate the complete dataset.
    jobs = load_jobs()

    all_rows = []
    # Generate samples for each career.
    for job in jobs:
        job_rows = make_samples_for_job(job)
        all_rows = all_rows + job_rows

    # Convert to DataFrame and shuffle rows.
    dataset = pd.DataFrame(all_rows)
    dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save the dataset to CSV.
    dataset.to_csv("data/training_data.csv", index=False)

    # Print summary statistics.
    print("Generated " + str(len(dataset)) + " samples for " + str(len(jobs)) + " careers")
    print(dataset["job_id"].value_counts())


if __name__ == "__main__":
    main()