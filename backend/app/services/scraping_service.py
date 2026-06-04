# app/services/scraping_service.py
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
# GENERIC VCARD EXTRACTION
# -----------------------------------

def extract_vcard_email(
    attorney_url,
    attorney_name
):

    try:

        print("\n==============================")
        print("GENERIC VCARD EXTRACTION")
        print("==============================")

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                channel="chrome"
            )

            context = browser.new_context(
                accept_downloads=True,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                )
            )

            page = context.new_page()

            page.goto(
                attorney_url,
                timeout=15000
            )

            page.wait_for_load_state("networkidle")
            # page.wait_for_timeout(3000)

            possible_selectors = [

                "text=vCard",
                "text=VCARD",
                "text=Download vCard",
                "text=Download Contact",
                "text=Add to Contacts",
                "text=Contact Card",

                "a[href*='vcf']",
                "a[href*='vcard']",

                "a:has-text('vCard')",
                "button:has-text('vCard')",

                "a:has-text('Download Contact')",
                "button:has-text('Download Contact')",

                "a:has-text('Add to Contacts')",
                "button:has-text('Add to Contacts')"

            ]

            vcard_button = None

            for selector in possible_selectors:

                try:

                    locator = page.locator(selector)

                    if locator.count() > 0:

                        vcard_button = locator.first
                        break

                except:
                    pass

            if not vcard_button:

                browser.close()

                return "Not Found"

            with page.expect_download(
                timeout=20000
            ) as download_info:

                vcard_button.click(force=True)

            download = download_info.value

            temp_dir = tempfile.gettempdir()

            vcf_path = os.path.join(
                temp_dir,
                download.suggested_filename
            )

            download.save_as(vcf_path)

            browser.close()

            with open(
                vcf_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                vcard_text = f.read()

            emails = extract_all_emails(
                vcard_text
            )

            email = select_best_email(
                emails,
                attorney_name
            )

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

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                channel="chrome"
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                )
            )

            page = context.new_page()

            print("\n===================================")
            print("SCRAPING PROFILE")
            print("===================================")

            print("URL:", url)
            print("Attorney:", attorney_name)

            page.goto(
                url,
                timeout=15000
            )

            page.wait_for_load_state("networkidle")
            # page.wait_for_timeout(3000)

            html = page.content()
            with open(
                f"debug_{attorney_name.replace(' ', '_')}.html",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(html)

            browser.close()

    except Exception as e:

        print("\nSCRAPING ERROR:")
        print(e)

        return {

            "title": "Error",

            "email": "Not Found",

            "phone": "Not Found",

            "bio": ""

        }

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
        "header",
        "footer"
    ]):
        tag.decompose()
        
    # -----------------------------------
    # MAILTO EMAIL EXTRACTION DEBUG
    # -----------------------------------

    mailto_emails = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if href.startswith("mailto:"):

            email_value = (
                href.replace("mailto:", "")
                .split("?")[0]
                .strip()
            )

            mailto_emails.append(email_value)

    print("\nMAILTO EMAILS:")
    print(mailto_emails)

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
    all_emails.extend(mailto_emails)

    all_emails = list(set(all_emails))
    
    print("\nALL EMAILS FOUND:")
    print(all_emails)

    email = select_best_email(
        all_emails,
        attorney_name
    )
    
    print("\nSELECTED EMAIL:")
    print(email)

    # -----------------------------------
    # GENERIC VCARD FALLBACK
    # -----------------------------------

    if email == "Not Found":

        vcard_email = extract_vcard_email(
            url,
            attorney_name
        )

        if vcard_email != "Not Found":

            email = vcard_email

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
            "practice",
            "litigation",
            "trademark",
            "licensing"

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