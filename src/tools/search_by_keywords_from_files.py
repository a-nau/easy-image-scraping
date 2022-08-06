import sys
from pathlib import Path

base_path = Path(__file__).parent.parent.parent
sys.path.append(base_path.as_posix())
from src.config import TARGET_PATH
from src.config import search_engines_per_language
from src.scraping.scrape_and_download import search_and_download
from src.scraping.utils import load_all_search_terms


def search_by_keywords_from_files():
    search_terms = load_all_search_terms()
    for language in search_engines_per_language.keys():
        for i, search_term in enumerate(search_terms[language]):
            for engine in search_engines_per_language[language]:
                folder_name = (
                    "_".join(search_terms["eng"][i].lower().split(" "))
                    + "_"
                    + language
                    + "_"
                    + engine
                )
                print("#" * 120)
                print("Searching for {}, saving in {}".format(search_term, folder_name))
                print("#" * 120)
                try:
                    search_and_download(
                        search_term,
                        TARGET_PATH,
                        number_images=100,
                        engine=engine,
                        folder_name=folder_name,
                    )
                except Exception as e:
                    print(f"Exception occurred: {e}")


if __name__ == "__main__":
    search_by_keywords_from_files()
