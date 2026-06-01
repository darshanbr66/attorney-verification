# app/services/confidence_service.py
def calculate_confidence(
    name_score,
    org_score
):

    final_score = (
        name_score * 0.6 +
        org_score * 0.4
    )

    return round(final_score, 2)