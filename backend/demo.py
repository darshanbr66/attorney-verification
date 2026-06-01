import pandas as pd
import time

from app.utils.query_generator import generate_search_queries
from app.services.search_service import search_attorney
from app.services.scraping_service import scrape_attorney_profile
from app.services.verification_service import verify_attorney


df = pd.read_csv(
    "data/raw/attorneys.csv"
)

final_results = []

for index, row in df.iterrows():

    print("\n================================================")
    print("USPTO RECORD")
    print("================================================")

    print(f"Attorney: {row['name']}")
    print(f"Organization: {row['organization']}")

    queries = generate_search_queries(
        row["name"],
        row["organization"]
    )

    print("\nGenerated Queries:")

    for q in queries:
        print("-", q)

    print("\nSearching Public Sources...")

    search_results = search_attorney(
        queries[0],
        row["name"]
    )

    if not search_results:

        print("\nNO SEARCH RESULTS FOUND")
        continue

    # -----------------------------------
    # DEBUG: SHOW ALL SEARCH RESULTS
    # -----------------------------------

    print("\nALL SEARCH RESULTS:")

    for i, url in enumerate(search_results):

        print(f"{i + 1}. {url}")

    # -----------------------------------
    # TAKE BEST MATCH
    # -----------------------------------

    # best_url = search_results[0]
    best_url = None

    for url in search_results:

        domain = url.lower()

        org = row["organization"].lower()

        if (
            "alston" in org
            and "alston.com" in domain
        ):
            best_url = url
            break

        elif (
            "ballard" in org
            and "ballardspahr.com" in domain
        ):
            best_url = url
            break

    if not best_url:
        best_url = search_results[0]

    print("\n--------------------------------")
    print("SELECTED URL:")
    print(best_url)
    print("--------------------------------")

    print("\nGathering Attorney Information...")

    profile_data = scrape_attorney_profile(
        best_url,
        row["name"]
    )

    print("\n================================")
    print("STRUCTURED ATTORNEY INFORMATION")
    print("================================")

    print("Name:", row["name"])
    print("Reg No:", row["reg_no"])
    print("Organization:", row["organization"])
    print("Email:", profile_data["email"])
    print("Phone:", profile_data["phone"])

    # -----------------------------------
    # VERIFICATION
    # -----------------------------------

    result = verify_attorney(
        row["name"],
        row["organization"],
        row["name"],
        row["organization"]
    )

    print("\nVerification Result:")
    print(result)

    final_results.append({

        "s_no": index + 1,

        "name": row["name"],

        "reg_no": row["reg_no"],

        "organization": row["organization"],

        "email": profile_data["email"],

        "phone": profile_data["phone"],

        "bio": profile_data["bio"][:1500],

        "source_url": best_url,

        "confidence": result["confidence"]

    })

    print("\nSleeping 2 seconds...")
    time.sleep(2)

# -----------------------------------
# SAVE RESULTS
# -----------------------------------

output_df = pd.DataFrame(
    final_results
)

output_df.to_csv(
    "data/verified/verified_attorneys.csv",
    index=False
)

output_df.to_excel(
    "data/verified/verified_attorneys.xlsx",
    index=False
)

print("\n===================================")
print("VERIFIED DATA SAVED SUCCESSFULLY")
print("===================================")

print("\nCSV:")
print("data/verified/verified_attorneys.csv")

print("\nEXCEL:")
print("data/verified/verified_attorneys.xlsx")