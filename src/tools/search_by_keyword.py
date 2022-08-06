import sys
from pathlib import Path

base_path = Path(__file__).parent.parent.parent
sys.path.append(base_path.as_posix())
from src.config import TARGET_PATH
from src.scraping.scrape_and_download import search_and_download


def search_by_keyword(search_term: str, search_engines: list = None, num_images=500):
    search_engines = (
        ["google", "yahoo", "baidu", "bing"]
        if search_engines is None
        else search_engines
    )
    for search_engine in search_engines:
        search_and_download(
            search_term,
            TARGET_PATH,
            number_images=num_images,
            engine=search_engine,
            folder_name="_".join(search_term.lower().split(" ")) + "_" + search_engine,
        )


if __name__ == "__main__":
    search_by_keyword("cardboard texture", search_engines=["google"], num_images=1)
