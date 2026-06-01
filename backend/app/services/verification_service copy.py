from app.ai.name_matcher import calculate_name_similarity
from app.ai.organization_matcher import calculate_org_similarity
from app.services.confidence_service import calculate_confidence

def verify_attorney(
    uspto_name,
    uspto_org,
    found_name,
    found_org
):

    name_score = calculate_name_similarity(
        uspto_name,
        found_name
    )

    org_score = calculate_org_similarity(
        uspto_org,
        found_org
    )

    confidence = calculate_confidence(
        name_score,
        org_score
    )

    return {
        "name_score": name_score,
        "org_score": org_score,
        "confidence": confidence
    }