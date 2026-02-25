import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scrape_txt import get_html

def extract_html_links(html):
    print("Looking for .html / .htm links...")
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = (a.get("href") or a.get("HREF") or "").strip()
        lower_href = href.lower()
        if lower_href.endswith(".html") or lower_href.endswith(".htm"):
            print(f"Found link: {href}")
            links.append(href)
        else:
            print(f"Skipping non-html: {href}")
    print(f"Total .html/.htm links found: {len(links)}")
    return links

def extract_body_html(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")
    if body:
        return str(body)
    return f"<body>{html}</body>"

def build_combined_html(base_url, first_html, links):
    soup = BeautifulSoup(first_html, "html.parser")
    head = soup.find("head")
    head_html = str(head) if head else "<head><meta charset='utf-8'></head>"
    bodies = []
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    for i, href in enumerate(links, 1):
        full_url = urljoin(base_url, href)
        print(f"[{i}/{len(links)}] Downloading: {href}")
        try:
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()
            body_html = extract_body_html(response.text)
            bodies.append(f"<!-- === {href} === -->\n{body_html}")
            print(f"Downloaded: {href} ({len(response.text)} bytes)")
        except Exception as e:
            print(f"Failed to download {href}: {e}")
    combined_body = "\n\n<hr>\n\n".join(bodies)
    return f"<!DOCTYPE html>\n<html>\n{head_html}\n{combined_body}\n</html>"

def save_combined(content):
    print("Saving combined HTML to combined.html...")
    with open("combined.html", "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("File saved")

if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    html = get_html(url)
    links = extract_html_links(html)
    if not links:
        print("No .html or .htm files found on the page")
    else:
        content = build_combined_html(url, html, links)
        save_combined(content)
    print("Finished")

