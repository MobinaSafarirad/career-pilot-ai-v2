# Converts the user's 20 answers into 0-10 scores for 12 skills using calibrated piecewise-linear mapping.

from data.skills import SKILL_LIST
from personality import QUESTIONS


def get_max_scores():
    # Initialize max_scores dictionary with zero for each skill.
    max_scores = {skill: 0 for skill in SKILL_LIST}
    # Iterate through each question to find the best possible contribution per skill.
    for question in QUESTIONS:
        # Track the highest points available for each skill in this question.
        best_this_question = {skill: 0 for skill in SKILL_LIST}
        # Check each option's weights to find the maximum for each skill.
        for option in question["options"]:
            # Compare each skill's points against the current best.
            for skill, points in option["weights"].items():
                # Update best if this option gives more points for this skill.
                if points > best_this_question[skill]:
                    best_this_question[skill] = points
        # Add the best per-question contribution to the running total for each skill.
        for skill in SKILL_LIST:
            max_scores[skill] += best_this_question[skill]
    # Return the dictionary of maximum possible raw scores.
    return max_scores


def _raw_score_distribution(skill):
    # Start with a distribution where raw score 0 has probability 1.0.
    dist = {0: 1.0}
    # Iterate through each question to convolve its contribution.
    for question in QUESTIONS:
        # Get the points contributed to this skill by each of the 4 options.
        contributions = [option["weights"].get(skill, 0) for option in question["options"]]
        # Initialize the next distribution.
        next_dist = {}
        # For each existing raw score and its probability...
        for raw, prob in dist.items():
            # For each possible contribution from the current question...
            for c in contributions:
                # Add the new raw score with the combined probability (each option has 0.25 probability).
                next_dist[raw + c] = next_dist.get(raw + c, 0.0) + prob * 0.25
        # Update the distribution to the next state.
        dist = next_dist
    # Return the exact distribution for this skill.
    return dist


def _scale_one_skill(raw, pivot, maximum):
    # Apply the piecewise-linear calibration function: 0->0, pivot->5, maximum->10.
    if raw <= pivot:
        # Avoid division by zero if pivot is 0.
        if pivot == 0:
            return 0.0
        # Scale linearly from 0 to 5.
        return 5.0 * (raw / pivot)
    else:
        # Calculate the range above the pivot.
        span = maximum - pivot
        # Avoid division by zero if pivot equals maximum.
        if span <= 0:
            return 10.0
        # Scale linearly from 5 to 10.
        return 5.0 + 5.0 * ((raw - pivot) / span)


def _expected_output(dist, pivot, maximum):
    # Calculate the expected (mean) output score given a raw score distribution, a pivot, and the maximum.
    return sum(prob * _scale_one_skill(raw, pivot, maximum) for raw, prob in dist.items())


def _solve_calibration_pivot(dist, maximum, target=5.0):
    # Find the pivot value that makes the expected output equal to the target using binary search.
    lo, hi = 1e-6, maximum - 1e-6
    # Perform 60 iterations of binary search for high precision.
    for _ in range(60):
        # Calculate the midpoint.
        mid = (lo + hi) / 2
        # Calculate the expected output at the midpoint and adjust bounds accordingly.
        if _expected_output(dist, mid, maximum) < target:
            # If output is below target, search the left half (lower pivot).
            hi = mid
        else:
            # Otherwise search the right half (higher pivot).
            lo = mid
    # Return the average of the final bounds as the pivot.
    return (lo + hi) / 2


def get_calibration_pivots():
    # Calculate the calibration pivot for each skill that makes average output 5.0.
    pivots = {}
    # For each skill, get its raw score distribution and calculate the pivot.
    for skill in SKILL_LIST:
        # Get the exact distribution of raw scores under random answering.
        dist = _raw_score_distribution(skill)
        # Solve for the pivot that makes the average output equal to 5.0.
        pivots[skill] = _solve_calibration_pivot(dist, MAX_SCORES[skill])
    # Return the dictionary of pivots.
    return pivots


# Calculate the maximum possible raw scores for each skill.
MAX_SCORES = get_max_scores()

# Calculate the calibration pivots for each skill.
CALIBRATION_PIVOTS = get_calibration_pivots()


def personality_to_skills(answers):
    # Convert a list of 20 answer choices (each 0, 1, 2, or 3) into a dictionary of 12 skill scores.
    # Validate that the number of answers matches the number of questions.
    if len(answers) != len(QUESTIONS):
        print("Error: wrong number of answers")
        return None
    # Initialize raw scores for all skills to 0.
    raw_scores = {skill: 0 for skill in SKILL_LIST}
    # Iterate through each question and add the points from the chosen option.
    for i in range(len(QUESTIONS)):
        # Get the current question and the chosen option.
        question = QUESTIONS[i]
        chosen = answers[i]
        option = question["options"][chosen]
        # For each skill affected by this choice, add the points to the raw score.
        for skill, points in option["weights"].items():
            raw_scores[skill] += points
    # Initialize a dictionary for the final calibrated scores.
    final_scores = {}
    # Convert raw scores to calibrated 0-10 scores for each skill.
    for skill in SKILL_LIST:
        # Apply the calibration function.
        score = _scale_one_skill(raw_scores[skill], CALIBRATION_PIVOTS[skill], MAX_SCORES[skill])
        # Clamp the score to the 0-10 range to guard against floating point errors.
        score = max(0.0, min(10.0, score))
        # Round to one decimal place for clean display and consistency.
        final_scores[skill] = round(score, 1)
    # Return the final skill scores.
    return final_scores


# Quick test to verify the module works correctly.
if __name__ == "__main__":
    # Test with all answers set to the first option.
    test_answers = [0] * len(QUESTIONS)
    # Print the resulting skill scores.
    print(personality_to_skills(test_answers))
