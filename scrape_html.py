import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scrape_txt import get_html

def extract_html_links(html):
    print("Looking for .html / .htm links...")
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href") or a.get("HREF")
        if href:
            href = href.strip()
            lower_href = href.lower()
            if lower_href.endswith(".html") or lower_href.endswith(".htm"):
                print(f"Found link: {href}")
                links.append(href)
            else:
                print(f"Skipping non-html: {href}")
    print(f"Total .html/.htm links found: {len(links)}")
    return links

def combine_html_texts(base_url, links):
    combined = ""
    for i, href in enumerate(links, 1):
        full_url = urljoin(base_url, href)
        print(f"[{i}/{len(links)}] Downloading: {href}")
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        try:
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()
            combined += f"--- {href} ---\n\n" + response.text + "\n\n\n"
            print(f"Downloaded: {href} ({len(response.text)} bytes)")
        except Exception as e:
            print(f"Failed to download {href}: {e}")
    return combined

def save_combined(content):
    print("Saving combined HTML content to combined_html.txt...")
    with open("combined_html.txt", "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("File saved")

if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    html = get_html(url)
    links = extract_html_links(html)
    if not links:
        print("No .html or .htm files found on the page")
    else:
        content = combine_html_texts(url, links)
        save_combined(content)
    print("Finished")
