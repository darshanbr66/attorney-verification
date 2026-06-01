from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import re
import tempfile
import os


# -----------------------------------
# EMAIL EXTRACTION
# -----------------------------------

def extract_all_emails(text):

    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    emails = re.findall(
        email_pattern,
        text
    )

    return list(set(emails))


# -----------------------------------
# SELECT BEST EMAIL
# -----------------------------------

def select_best_email(
    emails,
    attorney_name
):

    if not emails:
        return "Not Found"

    attorney_name = attorney_name.lower()

    name_parts = attorney_name.split()

    # Prefer attorney-specific email
    for email in emails:

        email_lower = email.lower()

        for part in name_parts:

            if len(part) > 2 and part in email_lower:
                return email

    # fallback
    return emails[0]


# -----------------------------------
# PHONE EXTRACTION
# -----------------------------------

def extract_phone(text):

    phone_pattern = r'''
        (?:
            \(\d{3}\)\s?\d{3}[-.\s]?\d{4}
            |
            \d{3}[-.\s]\d{3}[-.\s]\d{4}
            |
            \d{3}\.\d{3}\.\d{4}
        )
    '''

    phones = re.findall(
        phone_pattern,
        text,
        re.VERBOSE
    )

    return phones[0] if phones else "Not Found"


# -----------------------------------
# BOOTH UDALL VCARD EXTRACTION
# -----------------------------------
def extract_boothudall_vcard_email(
    attorney_url,
    attorney_name
):

    try:

        print("\n==============================")
        print("BOOTH UDALL VCARD EXTRACTION")
        print("==============================")

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False   # IMPORTANT FOR DEBUG
            )

            context = browser.new_context(
                accept_downloads=True
            )

            page = context.new_page()

            print("\nOpening URL:")
            print(attorney_url)

            page.goto(
                attorney_url,
                timeout=60000
            )

            page.wait_for_timeout(8000)

            print("\nPAGE TITLE:")
            print(page.title())

            print("\nALL LINKS FOUND:\n")

            links = page.locator("a").evaluate_all(
                """
                elements => elements.map(
                    e => ({
                        text: e.innerText,
                        href: e.href
                    })
                )
                """
            )

            for link in links:

                print(link)

            # -----------------------------------
            # FIND VCARD BUTTON
            # -----------------------------------

            vcard_button = None

            possible_selectors = [

                "text=vCard",
                "text=VCARD",
                "text=Download vCard",
                "a:has-text('vCard')",
                "button:has-text('vCard')"

            ]

            print("\nTRYING SELECTORS...\n")

            for selector in possible_selectors:

                try:

                    locator = page.locator(selector)

                    count = locator.count()

                    print(f"{selector} -> {count}")

                    if count > 0:

                        vcard_button = locator.first

                        print("\nVCARD BUTTON FOUND")
                        print("Selector:", selector)

                        break

                except Exception as e:

                    print(selector, "ERROR:", e)

            if not vcard_button:

                print("\nVCARD BUTTON NOT FOUND")

                browser.close()

                return "Not Found"

            # -----------------------------------
            # CLICK + DOWNLOAD
            # -----------------------------------

            print("\nCLICKING VCARD BUTTON...\n")

            with page.expect_download(
                timeout=20000
            ) as download_info:

                vcard_button.click(force=True)

            download = download_info.value

            print("DOWNLOAD TRIGGERED")

            temp_dir = tempfile.gettempdir()

            vcf_path = os.path.join(
                temp_dir,
                download.suggested_filename
            )

            download.save_as(vcf_path)

            print("\nDOWNLOADED FILE:")
            print(vcf_path)

            browser.close()

            # -----------------------------------
            # READ VCARD
            # -----------------------------------

            with open(
                vcf_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                vcard_text = f.read()

            print("\n===================")
            print("VCARD CONTENT")
            print("===================\n")

            print(vcard_text)

            emails = extract_all_emails(
                vcard_text
            )

            print("\nEMAILS FOUND:")
            print(emails)

            email = select_best_email(
                emails,
                attorney_name
            )

            print("\nFINAL EMAIL:")
            print(email)

            return email

    except Exception as e:

        print("\nVCARD ERROR:")
        print(e)

    return "Not Found"
# -----------------------------------
# MAIN SCRAPING FUNCTION
# -----------------------------------

def scrape_attorney_profile(
    url,
    attorney_name
):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            timeout=60000
        )

        # WAIT FOR JS RENDERING
        page.wait_for_timeout(5000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = (
        soup.title.string.strip()
        if soup.title
        else "No Title"
    )

    # REMOVE NOISY TAGS
    for tag in soup([
        "script",
        "style",
        "nav",
        "header"
    ]):
        tag.decompose()

    # -----------------------------------
    # FULL PAGE TEXT
    # -----------------------------------

    full_page_text = soup.get_text(
        separator=" ",
        strip=True
    )

    # -----------------------------------
    # EMAIL EXTRACTION
    # -----------------------------------

    all_emails = extract_all_emails(
        full_page_text
    )

    email = select_best_email(
        all_emails,
        attorney_name
    )

    # -----------------------------------
    # SPECIAL CASE:
    # BOOTH UDALL VCARD EXTRACTION
    # -----------------------------------

    if (
        email == "Not Found"
        and
        "boothudall" in url.lower()
    ):

        print("\nRUNNING BOOTH UDALL VCARD EXTRACTION...\n")

        email = extract_boothudall_vcard_email(
            url,
            attorney_name
        )

    # -----------------------------------
    # PHONE EXTRACTION
    # -----------------------------------

    phone = extract_phone(
        full_page_text
    )

    # -----------------------------------
    # BIO EXTRACTION
    # -----------------------------------

    paragraphs = soup.find_all("p")

    bio_text = ""

    capture = False

    for p in paragraphs:

        text = p.get_text(strip=True)

        if len(text) < 80:
            continue

        attorney_keywords = [
            "patent",
            "intellectual property",
            "clients",
            "technology",
            "practice"
        ]

        if any(
            keyword.lower() in text.lower()
            for keyword in attorney_keywords
        ):
            capture = True

        if capture:
            bio_text += text + "\n"

        if len(bio_text) > 2500:
            break

    if not bio_text:

        bio_text = full_page_text[:1500]

    return {

        "title": title,

        "email": email,

        "phone": phone,

        "bio": bio_text

    }