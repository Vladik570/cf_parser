from bs4 import BeautifulSoup
from pathlib import Path

def collect_token_links_from_file(file_path: str) -> list[str]:
    html = Path(file_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html,"lxml")

    links = []

    table = soup.find("table")
    if table is None:
        return links

    tbody = table.find("tbody")
    if tbody is None:
        return links

    for row in tbody.find_all("tr"):
        a_tag = row.find("a", href=True)
        if a_tag is None:
            continue

        href = a_tag["href"]
        if not href.startswith('/currencies/'):
            continue
        clean_href = href.split('#')[0]
        full_url = "https://www.coinmarketcap.com" + clean_href

        if full_url not in links:
            links.append(full_url)


    return links
