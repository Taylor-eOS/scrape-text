import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_html(url):
    print("Fetching main page...")
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print("Main page fetched")
    return response.text

def extract_txt_links(html):
    print("Looking for .txt links...")
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href") or a.get("HREF")
        if href:
            href = href.strip()
            if href.lower().endswith(".txt"):
                print(f"Found link: {href}")
                links.append(href)
            elif href.lower().endswith((".html", ".htm", "/")) or not "." in href.split("/")[-1]:
                print(f"Skipping non-txt: {href}")
    print(f"Total .txt links found: {len(links)}")
    return links

def combine_texts(base_url, links):
    combined = ""
    for i, href in enumerate(links, 1):
        full_url = urljoin(base_url, href)
        print(f"[{i}/{len(links)}] Downloading: {href}")
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        try:
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()
            combined += response.text + "\n\n"
            print(f"Downloaded: {href} ({len(response.text)} bytes)")
        except Exception as e:
            print(f"Failed to download {href}: {e}")
    return combined

def save_combined(content):
    print("Saving combined text to combined.txt...")
    with open("combined.txt", "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("File saved")

if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    html = get_html(url)
    links = extract_txt_links(html)
    if not links:
        print("No .txt files found on the page")
    else:
        content = combine_texts(url, links)
        save_combined(content)
    print("Finished")

