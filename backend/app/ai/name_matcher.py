
# name_matcher.py
from rapidfuzz import fuzz

def calculate_name_similarity(name1, name2):

    score = fuzz.ratio(
        name1.lower(),
        name2.lower()
    )

    return score