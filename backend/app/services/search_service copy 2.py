from ddgs import DDGS


def is_valid_profile_url(url):

    valid_patterns = [

        "/professionals/",
        "/people/",
        "/attorneys/",
        "/team-member/",
        "/lawyers/",
        "/person/",
        "/our-team/",
        "/team/",
        "/professionals-detail/"

    ]

    blocked_patterns = [

        "article",
        "news",
        "event",
        "blog",
        "insights",
        "dallasinnovates",
        "linkedin",
        "facebook",
        "twitter",
        "instagram"

    ]

    url_lower = url.lower()

    # BLOCK BAD URLS
    for blocked in blocked_patterns:

        if blocked in url_lower:
            return False

    # ALLOW STANDARD PROFILE URLS
    for valid in valid_patterns:

        if valid in url_lower:
            return True

    return False


def search_attorney(
    query,
    attorney_name
):

    urls = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=10
            )

            for r in results:

                if "href" not in r:
                    continue

                url = r["href"]

                url_lower = url.lower()

                # STANDARD VALIDATION
                if is_valid_profile_url(url):

                    urls.append(url)
                    continue

                # --------------------------------
                # FALLBACK:
                # ATTORNEY NAME INSIDE URL
                # --------------------------------

                attorney_parts = attorney_name.lower().split()

                matched_parts = 0

                for part in attorney_parts:

                    if len(part) > 2 and part in url_lower:
                        matched_parts += 1

                # if at least 2 name parts match
                if matched_parts >= 2:

                    urls.append(url)

    except Exception as e:

        print("Search Error:", e)

    return urls