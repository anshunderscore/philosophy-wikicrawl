"""
Script to automate the Wikipedia philosophy game

Rules:
1. Clicking on the first non-parenthesized, non-italicized link
2. Ignoring external links, links to the current page, or red links
3. Stopping when: reaching "Philosophy" / a page without links / if a loop occurs
"""


import copy
import re
from types import NoneType
import webbrowser
import requests


START_PAGE = "/wiki/Special:Random"
pages = set()


def get_first_link(wiki_page: str) -> str:
    """Get the first non-parenthesized, non-italicized link in the main body"""

    html = requests.get(f"https://wikipedia.org/{wiki_page}").text
    link = re.search(r"<p>.*?href=\"(\/wiki\/[^:]*?)\"", html, flags=re.MULTILINE)
    return None if isinstance(link, NoneType) else link[1]


def crawl():
    """Go to every first link and get a new one until it's /wiki/Philosophy """

    wiki_page = copy.copy(START_PAGE)
    i = 0

    while wiki_page != "/wiki/philosophy":
        i += 1
        wiki_page = get_first_link(wiki_page)
        if wiki_page is None:
            raise Exception("Arrived at a page with no links")
        elif wiki_page in pages:
            raise Exception("Stuck in a loop")
        pages.add(wiki_page)       
        yield wiki_page


if __name__ == "__main__":
    for wiki_page in crawl():
        webbrowser.open(f"https://wikipedia.org/{wiki_page}")
