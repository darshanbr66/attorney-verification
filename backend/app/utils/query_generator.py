# app/utils/query_generator.py

def generate_search_queries(
    name,
    organization="",
    city=""
):

    queries = []

    # Strongest query
    if organization and city:

        queries.append(
            f"{name} {organization} {city} patent attorney"
        )

    # Name + Organization
    if organization:

        queries.append(
            f"{name} {organization} patent attorney"
        )

        queries.append(
            f"{name} {organization} intellectual property lawyer"
        )

        queries.append(
            f'"{name}" "{organization}"'
        )

    # Name + City
    if city:

        queries.append(
            f"{name} {city} patent attorney"
        )

        queries.append(
            f"{name} {city} intellectual property lawyer"
        )

        queries.append(
            f'"{name}" "{city}"'
        )

    # Fallbacks
    queries.append(
        f"{name} patent attorney"
    )

    queries.append(
        f"{name} intellectual property lawyer"
    )

    # Remove duplicates while preserving order
    unique_queries = []

    for query in queries:

        if query not in unique_queries:

            unique_queries.append(query)

    return unique_queries