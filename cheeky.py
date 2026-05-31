import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv
import time

category_urls = [
    "https://ssmu.ca/clubs/athletics-recreation-clubs/",
    "https://ssmu.ca/clubs/charity-environment-clubs/",
    "https://ssmu.ca/clubs/community-outreach-and-volunteering-clubs/",
    "https://ssmu.ca/clubs/performing-finearts-clubs/",
    "https://ssmu.ca/clubs/health-wellness-clubs/",
    "https://ssmu.ca/clubs/language-publications/",
    "https://ssmu.ca/clubs/hobby-leisure-clubs/",
    "https://ssmu.ca/clubs/networking-and-leadership-development-clubs/",
    "https://ssmu.ca/clubs/political-socialactivism-clubs/",
    "https://ssmu.ca/clubs/religion-culture-clubs/",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

club_links = set()
emails = []

email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Step 1: collect club links
for url in category_urls:
    print(f"Scanning category: {url}")
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/clubs/" in href and href.startswith("https://ssmu.ca/clubs/"):
            club_links.add(href)

print(f"Found {len(club_links)} club pages")

# Step 2: scrape emails
for link in sorted(club_links):
    if len(emails) >= 200:
        break

    try:
        print(f"Checking {link}")

        r = requests.get(link, headers=headers, timeout=10)
        page = r.text

        found = set(email_pattern.findall(page))

        found = {
            e for e in found
            if "@" in e
            and "png" not in e
            and "jpg" not in e
        }

        for email in found:
            emails.append([link, email])

            if len(emails) >= 200:
                break

        time.sleep(0.5)

    except Exception as e:
        print("Error:", e)

# dedupe
unique = []
seen = set()

for row in emails:
    if row[1] not in seen:
        seen.add(row[1])
        unique.append(row)

# save CSV
with open("ssmu_club_emails.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Club Page", "Email"])
    writer.writerows(unique[:200])

print(f"Saved {len(unique[:200])} emails to ssmu_club_emails.csv")
