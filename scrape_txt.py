import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def extract_txt_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href") or a.get("HREF")
        if href and href.lower().endswith(".txt"):
            links.append(href.strip())
    return links

def combine_texts(base_url, links):
    combined = ""
    for href in links:
        full_url = urljoin(base_url, href)
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()
        combined += response.text + "\n\n"
    return combined

def save_combined(content):
    with open("combined.txt", "w", encoding="utf-8") as f:
        f.write(content.strip())

if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    html = get_html(url)
    links = extract_txt_links(html)
    content = combine_texts(url, links)
    save_combined(content)

