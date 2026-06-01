from app.services.search_service import search_attorney
from app.services.scraping_service import scrape_attorney_profile
from app.utils.query_generator import generate_search_queries
from app.services.verification_service import verify_attorney


def extract_organization_from_title(title):

    if not title:
        return ""

    separators = [
        "|",
        "-",
        "—",
        ","
    ]

    for sep in separators:

        if sep in title:

            parts = title.split(sep)

            if len(parts) > 1:
                return parts[-1].strip()

    return title.strip()


def verify_single_attorney(
    name,
    reg_no="",
    organization="",
    city=""
):

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

                found_org = (
                    extract_organization_from_title(
                        title
                    )
                )

                verification = verify_attorney(
                    uspto_name=name,
                    uspto_org=organization,
                    found_name=name,
                    found_org=found_org
                )

                confidence = verification[
                    "confidence"
                ]

                if email != "Not Found":
                    confidence += 3

                if phone != "Not Found":
                    confidence += 2

                confidence = min(
                    confidence,
                    100
                )

                if confidence > best_confidence:

                    best_confidence = confidence

                    best_result = {

                        "name": name,

                        "reg_no": reg_no,

                        "organization": organization,

                        "city": city,

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

            except Exception as e:

                print(
                    f"\nPROFILE ERROR: {e}"
                )

                continue

    if best_result:

        print("\nBEST MATCH FOUND")

        return best_result

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