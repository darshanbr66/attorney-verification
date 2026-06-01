# organization_matcher.py
from rapidfuzz import fuzz

def calculate_org_similarity(org1, org2):

    score = fuzz.ratio(
        org1.lower(),
        org2.lower()
    )

    return score