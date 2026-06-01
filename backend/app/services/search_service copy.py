from ddgs import DDGS

def search_attorney(query):

    urls = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=5
            )

            for r in results:

                if "href" in r:

                    urls.append(
                        r["href"]
                    )

    except Exception as e:

        print("Search Error:", e)

    return urls