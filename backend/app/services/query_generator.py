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

        queries.append(
            f"{name} {organization} intellectual property lawyer"
        )

    if city:

        queries.append(
            f"{name} {city} patent attorney"
        )

    queries.append(
        f"{name} patent attorney"
    )

    queries.append(
        f"{name} intellectual property lawyer"
    )

    return queries