from pathlib import Path

language_list = ["cn", "eng", "ger"]
search_engines_per_language = {
    # 'cn': ['baidu'],
    "eng": ["google", "bing"],
    "ger": ["google", "bing"],  # not using Yahoo since only low-res is possible
}
search_term_file_base = "search_terms_"
ROOT_PATH = Path(__file__).parent.parent
TARGET_PATH = ROOT_PATH / "output"
