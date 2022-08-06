import csv
import datetime
import hashlib
import io
import os

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.config import ROOT_PATH
from src.scraping.fetch_image_urls import fetch_image_urls


def set_chrome_options() -> Options:
    """
    # From https://nander.cc/using-selenium-within-a-docker-container
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=chrome")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_extension(
        ROOT_PATH / "data/extensions/I-don-t-care-about-cookies.crx"
    )
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def search_and_download(
    search_term: str,
    target_path="./output",
    number_images=5,
    engine="google",
    folder_name=None,
):
    target_folder = create_target_folder(folder_name, target_path, search_term)

    if target_folder is not None:
        with webdriver.Chrome(
            options=set_chrome_options()
        ) as wd:  # note: could pass local driver path here
            img_urls = fetch_image_urls(
                search_term, number_images, wd=wd, engine=engine
            )

        save_img_urls(img_urls, target_folder)


def create_target_folder(folder_name, target_path, search_term):
    if folder_name:
        target_folder = os.path.join(target_path, folder_name)
    else:
        target_folder = os.path.join(
            target_path, "_".join(search_term.lower().split(" "))
        )

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        return target_folder
    else:
        print(
            f"Folder {target_folder} for search term {search_term} already exists. Skipping."
        )
        return None


def persist_image(folder_path: str, url: str):
    try:
        image_content = requests.get(url).content
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert("RGB")
            file_path = os.path.join(
                folder_path, hashlib.sha1(image_content).hexdigest()[:10] + ".jpg"
            )
            with open(file_path, "wb") as f:
                image.save(f, "JPEG", quality=100)
            return ["success", url, file_path]
        except Exception as e:
            return ["failure", url, e]
    except Exception as e:
        return ["failure", url, e]


def save_img_urls(img_urls, target_folder):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(
        os.path.join(target_folder, timestamp + "_log.csv"), "w", newline=""
    ) as log:
        write = csv.writer(log)
        write.writerow(["Success", "URL", "Image Path"])
        for i, elem in enumerate(img_urls):
            log_data = persist_image(target_folder, elem)
            if log_data[0] == "success":
                print(
                    f"{str(i + 1).zfill(3)}/{len(img_urls)} - SUCCESS - saved {log_data[1]} - as {log_data[2]}"
                )
            else:
                print(
                    f"{str(i + 1).zfill(3)}/{len(img_urls)} - ERROR - Could not save {log_data[1]} - {log_data[2]}"
                )
            write.writerow(log_data)
