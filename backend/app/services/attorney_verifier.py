import re

from app.services.search_service import search_attorney
from app.services.scraping_service import (
    scrape_attorney_profile,
    normalize_organization
)
from app.utils.query_generator import generate_search_queries
from app.services.verification_service import verify_attorney

def extract_organization_from_title(title):

    if not title:
        return ""

    parts = [
        part.strip()
        for part in re.split(r"[|\-—]", title)
    ]

    for part in parts:

        lower_part = part.lower()

        # Skip obvious attorney names
        if "." in part:
            continue

        # Skip legal topic text
        if any(
            keyword in lower_part
            for keyword in [
                "patent",
                "trademark",
                "intellectual property",
                "people",
                "professionals"
            ]
        ):
            continue

        if len(part) < 3:
            continue

        return part

    return ""

def verify_single_attorney(
    name,
    reg_no="",
    organization="",
    city=""
):
    import time

    print("\n" + "=" * 60)
    print("NEW REQUEST STARTED")
    print("TIME:", time.strftime("%H:%M:%S"))
    print("=" * 60)

    best_result = None
    best_confidence = 0

    print("\n" + "=" * 60)
    print("ATTORNEY VERIFICATION STARTED")
    print("=" * 60)

    print(f"NAME: {name}")
    print(f"REG NO: {reg_no}")
    print(f"ORG: {organization}")
    print(f"CITY: {city}")

    # ---------------------------------
    # GENERATE SEARCH QUERIES
    # ---------------------------------

    queries = generate_search_queries(
        name=name,
        organization=organization,
        city=city
    )

    print("\nGENERATED QUERIES:")

    for q in queries:
        print("•", q)

    # ---------------------------------
    # SEARCH EACH QUERY
    # ---------------------------------

    for query in queries:

        print("\n" + "-" * 60)
        print("SEARCHING:")
        print(query)
        print("-" * 60)

        urls = search_attorney(
            query,
            name
        )

        if not urls:
            continue

        # Optional:
        # Only check first few URLs
        urls = urls[:2]

        for url in urls:

            try:

                print("\nSCRAPING URL:")
                print(url)

                scraped = scrape_attorney_profile(
                    url,
                    name
                )

                title = scraped.get(
                    "title",
                    ""
                )

                email = scraped.get(
                    "email",
                    "Not Found"
                )

                phone = scraped.get(
                    "phone",
                    "Not Found"
                )

                bio = scraped.get(
                    "bio",
                    ""
                )
                detected_city = scraped.get(
                    "city",
                    ""
                )

                found_org = scraped.get(
                    "organization",
                    ""
                )

                if not found_org:

                    found_org = (
                        extract_organization_from_title(
                            title
                        )
                    )

                found_org = normalize_organization(
                    found_org,
                    url
                )

                verification = verify_attorney(
                    uspto_name=name,
                    uspto_org=organization,
                    found_name=name,
                    found_org=organization
                )

                confidence = verification[
                    "confidence"
                ]

                # -----------------------------
                # BONUS CONFIDENCE
                # -----------------------------

                if email != "Not Found":
                    confidence += 3

                if phone != "Not Found":
                    confidence += 2

                confidence = min(
                    confidence,
                    100
                )

                print(
                    f"CONFIDENCE: {confidence}"
                )

                result = {

                    "name": name,

                    "reg_no": reg_no,

                    "organization": organization if organization else found_org,

                    "city": detected_city if detected_city else city,

                    "email": email,

                    "phone": phone,

                    "source_url": url,

                    "confidence": round(
                        confidence,
                        2
                    ),

                    "page_title": title,

                    "detected_organization":
                    found_org,

                    "bio": bio[:1000]

                }

                # -----------------------------
                # HIGH CONFIDENCE
                # RETURN IMMEDIATELY
                # -----------------------------

                if confidence >= 75:

                    print(
                        "\nHIGH CONFIDENCE MATCH FOUND"
                    )

                    print("\nRESULT:")
                    print(result)

                    return result

                # -----------------------------
                # SAVE BEST RESULT
                # -----------------------------

                if confidence > best_confidence:

                    best_confidence = confidence

                    best_result = result

            except Exception as e:

                print(
                    f"\nPROFILE ERROR: {e}"
                )

                continue

    # ---------------------------------
    # RETURN BEST MATCH
    # ---------------------------------

    if best_result:

        print("\nBEST MATCH FOUND")

        return best_result

    # ---------------------------------
    # NO MATCH
    # ---------------------------------

    return {

        "name": name,

        "reg_no": reg_no,

        "organization": organization,

        "city": city,

        "email": "Not Found",

        "phone": "Not Found",

        "source_url": "",

        "confidence": 0,

        "page_title": "",

        "detected_organization": "",

        "bio": ""

    }