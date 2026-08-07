def calculate_compliance(
    documentation,
    bias_testing,
    privacy_assessment,
    human_oversight,
    explainability,
    security_testing,
):

    score = 0

    if documentation:
        score += 20

    if bias_testing:
        score += 15

    if privacy_assessment:
        score += 20

    if human_oversight:
        score += 15

    if explainability:
        score += 15

    if security_testing:
        score += 15

    return score