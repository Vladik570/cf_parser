from bs4 import BeautifulSoup
from pathlib import Path
import re

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

def collect_token_info(file_path: str) -> dict:
    html = Path(file_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    name, ticker = get_name_and_ticker(soup)
    socials = get_socials(soup)
    website = get_website(soup)
    return {
        "name": name,
        "ticker": ticker,
        "socials": socials,
        "website": website,
    }

def get_name_and_ticker(soup) -> tuple[str | None, str | None]:
    name = None
    ticker = None

    h1 = soup.find("h1")

    if h1:
        parts = list(h1.stripped_strings)

        if parts:
            name = parts[0]

        for part in parts[1:]:
            if re.fullmatch(r"[A-Z0-9]{2,15}", part):
                ticker = part
                break

    return name, ticker


def get_website(soup) -> str | None:
    web_tag = soup.select_one('a[data-test="chip-website-link"]')

    if web_tag and web_tag.get("href"):
        url = web_tag["href"]
        if url.startswith("//"):
            url = "https:" + url
        return url

    return None

def get_socials(soup) -> list[str]:
    block = soup.select_one('div[class*="CoinInfoLinks"]')
    if not block:
        return []

    socials_domains = (
        "twitter.com",
        "x.com",
        "t.me",
        "telegram",
        "discord",
        "github.com",
        "medium.com",
        "facebook.com",
        "instagram.com",
    )

    links = []
    for a in block.select("a[href]"):
        href = a.get("href", "")

        if any(domain in href for domain in socials_domains):
            links.append(href)

    return list(set(links))