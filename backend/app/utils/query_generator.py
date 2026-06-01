# utils/query_generator.py
def generate_search_queries(
    name,
    organization="",
    city=""
):

    queries = []

    if organization:

        queries.append(
            f"{name} {organization} patent attorney"
        )

    if city:

        queries.append(
            f"{name} {city} patent attorney"
        )

    queries.append(
        f"{name} patent attorney"
    )

    return queries