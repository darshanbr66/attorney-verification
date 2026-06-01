def generate_search_queries(name, organization):

    queries = []

    queries.append(
        f"{name} {organization} patent attorney"
    )

    queries.append(
        f"{name} {organization} intellectual property lawyer"
    )

    queries.append(
        f"{name} site:linkedin.com/in"
    )

    return queries