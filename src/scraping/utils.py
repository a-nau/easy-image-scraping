from typing import List, Dict
from src.config import search_engines_per_language, search_term_file_base, ROOT_PATH


def load_all_search_terms() -> Dict[str, List]:
    search_terms = {}
    for language in search_engines_per_language.keys():
        search_terms[language] = read_txt(
            (ROOT_PATH / "data" / f"{search_term_file_base}{language}.txt").as_posix()
        )
    return search_terms


def read_txt(filename) -> List[str]:
    with open(filename, encoding="utf8") as f:
        search_term_list = f.read().splitlines()
    return search_term_list
