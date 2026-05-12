from bs4 import BeautifulSoup
from pathlib import Path

def collect_token_links_from_file(file_path: str) -> list[str]:
    html = Path(file_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html,"lxml")

    links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        if href.startswith("/currencies/"):
            full_url = "https://coinmarketcap.com" + href

            if full_url not in links:
                links.append(full_url)

    return links
