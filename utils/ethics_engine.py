def calculate_ethics_score(
    fairness,
    transparency,
    accountability,
    explainability,
    privacy,
    human_oversight,
):

    score = 0

    if fairness:
        score += 20

    if transparency:
        score += 15

    if accountability:
        score += 15

    if explainability:
        score += 15

    if privacy:
        score += 20

    if human_oversight:
        score += 15

    return score