def calculate_risk(
    personal_data,
    automated_decision,
    biometric_data,
    human_oversight,
    employment,
):

    score = 0

    if personal_data:
        score += 20

    if automated_decision:
        score += 25

    if biometric_data:
        score += 25

    if not human_oversight:
        score += 20

    if employment:
        score += 10

    if score >= 70:
        level = "High"

    elif score >= 40:
        level = "Medium"

    else:
        level = "Low"

    return score, level