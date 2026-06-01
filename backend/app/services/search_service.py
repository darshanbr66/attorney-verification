# app/services/search_service.py
from ddgs import DDGS


# -----------------------------------
# VALID PROFILE URL FILTER
# -----------------------------------

def is_valid_profile_url(url):

    valid_patterns = [

        "/professionals/",
        "/people/",
        "/attorneys/",
        "/team-member/",
        "/lawyers/",
        "/lawyer/",
        "/person/",
        "/our-team/",
        "/team/",
        "/bio/",
        "/our-people/",
        "/professionals-detail/",
        "/en/lawyers/",
        "/lawyers/t/",
        "/attorney/"

    ]

    blocked_patterns = [

        "article",
        "news",
        "event",
        "blog",
        "insights",
        "linkedin",
        "facebook",
        "twitter",
        "instagram",
        "youtube",
        "wikipedia"

    ]

    url_lower = url.lower()

    # BLOCK BAD URLS
    for blocked in blocked_patterns:

        if blocked in url_lower:
            return False

    # ALLOW VALID PROFILE URLS
    for valid in valid_patterns:

        if valid in url_lower:
            return True

    return False


# -----------------------------------
# SEARCH ATTORNEY
# -----------------------------------

def search_attorney(
    query,
    attorney_name
):

    urls = []

    blocked_patterns = [

        "article",
        "news",
        "event",
        "blog",
        "insights",
        "linkedin",
        "facebook",
        "twitter",
        "instagram",
        "youtube",
        "wikipedia"

    ]
    
    blocked_domains = [

        "plainsite.org",
        "bestlawyers.com",
        "bestlawfirms.com",
        "jdsupra.com",
        "legal500.com",
        "firmprospects.com",
        "patentbots.com",
        "linkedin.com",
        "zoominfo.com",
        "findlaw.com",
        "superlawyers.com",
        "lawyer.com",
        "chambers.com"

    ]

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
                
                # -----------------------------------
                # BLOCK THIRD-PARTY DIRECTORY SITES
                # -----------------------------------

                skip_url = False

                for domain in blocked_domains:

                    if domain in url_lower:

                        skip_url = True
                        break

                if skip_url:

                    print("BLOCKED DOMAIN:", url)

                    continue

                print("\nFOUND URL:")
                print(url)

                # -----------------------------------
                # STANDARD VALIDATION
                # -----------------------------------

                if is_valid_profile_url(url):

                    print("VALID PROFILE URL")

                    urls.append(url)

                    continue

                # -----------------------------------
                # FALLBACK:
                # ATTORNEY NAME INSIDE URL
                # -----------------------------------

                attorney_parts = attorney_name.lower().split()

                matched_parts = 0

                for part in attorney_parts:

                    if len(part) > 2 and part in url_lower:

                        matched_parts += 1

                # -----------------------------------
                # REQUIRE MINIMUM MATCH
                # -----------------------------------

                if matched_parts >= 2:

                    # -----------------------------------
                    # RECHECK BLOCKED URLS
                    # -----------------------------------

                    blocked = False

                    for blocked_word in blocked_patterns:

                        if blocked_word in url_lower:

                            blocked = True
                            break

                    if not blocked:

                        print("FALLBACK URL ACCEPTED")

                        urls.append(url)

    except Exception as e:

        print("\nSEARCH ERROR:")
        print(e)

    return urls