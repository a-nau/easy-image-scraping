import os
import random
import sys
from pathlib import Path

import streamlit as st

base_path = Path(__file__).parent.parent.parent
sys.path.append(base_path.as_posix())

from src.config import TARGET_PATH
from src.tools.search_by_keyword import search_by_keyword


def main():
    # Info
    st.set_page_config(page_title="Image Scraping Tool")
    st.markdown(
        f"<h1 style='text-align: center; '>Image Scraping Tool</h1>",
        unsafe_allow_html=True,
    )

    # Config
    search_engines = ["Google", "Bing", "Baidu", "Yahoo"]
    selected_search_engines = st.multiselect(
        "Search Engines", search_engines, default=search_engines[:-1]
    )
    search_query = st.text_input("Search Query (separate by ;)")
    num_images = st.slider(
        "Number of Images to Download", min_value=1, max_value=500, value=10
    )
    clear_output = st.checkbox("Clear Output Folder", value=False, help="Remove all files and folders in output folder.")

    # Run search
    if st.button("Start Search", disabled=search_query == ""):
        if clear_output:
            clear_output_folder()
        for query in search_query.split(";"):
            query = query.strip()
            search_by_keyword(
                query, [s.lower() for s in selected_search_engines], num_images
            )
            query_folders = [
                f for f in (base_path / "output").glob(f"{query}*") if f.is_dir()
            ]
            for folder in query_folders:
                ex = st.expander(f"Samples from {folder.name}")
                images = [
                    f.as_posix()
                    for f in folder.glob("*")
                    if f.suffix in [".gif", ".png", ".jpg", ".jpeg"]
                ]
                images_sample = random.sample(images, min(len(images), 20))
                ex.image(images_sample, width=200)

def clear_output_folder():
    if not os.path.isdir(TARGET_PATH):
        return
    for root, dirs, files in os.walk(TARGET_PATH, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    print(f"Output folder cleared.")

if __name__ == "__main__":
    main()
