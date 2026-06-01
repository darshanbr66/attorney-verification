import pandas as pd

from app.utils.query_generator import generate_search_queries
from app.services.search_service import search_attorney
from app.services.scraping_service import scrape_attorney_profile
from app.services.verification_service import verify_attorney


df = pd.read_csv(
    "data/raw/attorneys.csv"
)

# FINAL OUTPUT STORAGE
final_results = []

for index, row in df.iterrows():

    print("\n====================")
    print("USPTO RECORD")
    print("====================")

    print(f"Attorney: {row['name']}")
    print(f"Organization: {row['organization']}")

    queries = generate_search_queries(
        row['name'],
        row['organization']
    )

    print("\nGenerated Queries:")

    for q in queries:
        print("-", q)

    print("\nSearching Public Sources...")

    search_results = search_attorney(
        queries[0],
        row['name']
    )

    if not search_results:

        print("No search results found.")
        continue

    # TAKE BEST MATCH ONLY
    best_url = search_results[0]

    print("\n--------------------------------")
    print("Candidate URL:")
    print(best_url)

    print("\nGathering Attorney Information...")

    profile_data = scrape_attorney_profile(
        best_url,
        row['name'],
        # row['organization']
    )

    print("\nStructured Attorney Information:\n")

    print("Name:", row['name'])
    print("Reg No:", row['reg_no'])
    print("Organization:", row['organization'])
    print("Email:", profile_data["email"])
    print("Phone:", profile_data["phone"])

    print("\nBio:\n")
    print(profile_data["bio"][:1000])

    # NLP Verification
    result = verify_attorney(
        row['name'],
        row['organization'],
        row['name'],
        row['organization']
    )

    print("\nVerification Result:")
    print(result)

    # STORE STRUCTURED DATA
    final_results.append({

        "s_no": index + 1,

        "name": row['name'],

        "reg_no": row['reg_no'],

        "organization": row['organization'],

        "email": profile_data["email"],

        "phone": profile_data["phone"],

        "bio": profile_data["bio"][:1500],

        "source_url": best_url,

        "confidence": result["confidence"]

    })


# SAVE CSV
output_df = pd.DataFrame(
    final_results
)

output_df.to_csv(
    "data/verified/verified_attorneys.csv",
    index=False
)

# SAVE EXCEL
output_df.to_excel(
    "data/verified/verified_attorneys.xlsx",
    index=False
)

print("\n===================================")
print("VERIFIED DATA SAVED SUCCESSFULLY")
print("===================================")

print("\nCSV File:")
print("data/verified/verified_attorneys.csv")

print("\nExcel File:")
print("data/verified/verified_attorneys.xlsx")
