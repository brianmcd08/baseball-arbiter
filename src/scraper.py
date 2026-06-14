import requests
import time
from bs4 import BeautifulSoup

from src.schema import RuleChunk
from config import mlb_rulebook_url, scraper_timeout, mlb_schema


def scraper():
    rule_chunks = []
    response = requests.get(url=mlb_rulebook_url, timeout=scraper_timeout)
    landing_page = BeautifulSoup(response.text, "html.parser")

    sections = landing_page.select(".p-related-links__list a")
    for section in sections:
        rc = RuleChunk(
            rule_name=section.text,  # could be in the next loop
            url=mlb_schema + section["href"],
            content="",
            subsection=None,
        )
        rule_chunks.append(rc)

    rule_chunks_final = []
    for rule_chunk in rule_chunks:
        time.sleep(2)
        response = requests.get(url=rule_chunk.url, timeout=scraper_timeout)
        soup = BeautifulSoup(response.text, "html.parser")

        h3_tags = soup.find_all("h3")
        for h3 in h3_tags:
            heading_text = h3.text.strip()

            current_element = h3.next_sibling
            while current_element:
                if current_element.name in ["h1", "h2", "h3", "h4", "h5"]:
                    break

                if current_element.name == "p":
                    current_text = current_element.text.strip()
                    if not (
                        len(current_text) < 20
                        and current_text[-1] not in [".", "?", "!"]
                    ):
                        rc = RuleChunk(
                            rule_name=rule_chunk.rule_name,  # could be in the next loop
                            url=rule_chunk.url,
                            content=current_text,
                            subsection=heading_text,
                        )
                        print("ok")
                        rule_chunks_final.append(rc)
                current_element = current_element.next_sibling

    # print(f"Total chunks: {len(rule_chunks_final)}")
    # print(f"Empty content: {sum(1 for c in rule_chunks_final if not c.content)}")
    # print(f"No subsection: {sum(1 for c in rule_chunks_final if c.subsection is None)}")
    # print(
    #     f"With subsection: {sum(1 for c in rule_chunks_final if c.subsection is not None)}"
    # )


if __name__ == "__main__":
    scraper()
