import json
import random
import time
from urllib.parse import urlencode, urlparse, parse_qs


from selenium import webdriver
from selenium.webdriver.common.by import By


def search_engine_factory(name, wd):
    if name.lower() == "google":
        search_engine = SearchGoogle(wd)
    elif name.lower() == "bing":
        search_engine = SearchBing(wd)
    elif name.lower() == "baidu":
        search_engine = SearchBaidu(wd)
    elif name.lower() == "yahoo":
        search_engine = SearchYahoo(wd)
    else:
        raise ValueError(f"Search engine {name} is not implemented!")
    return search_engine


class Search:
    def __init__(self, wd: webdriver.Chrome):
        self.wd = wd
        self.sleep_between_interactions = [0.5, 1.5]
        self.url = ""
        self.accepted_privacy_notice = False

    def load_search(self, query):
        if self.url == "":
            print("No valid search")
        else:
            self.wd.get(self.url.format(q=query))

    def find_thumbnail_elements(self):
        raise NotImplementedError("Must be implemented by subclass")

    def get_image_urls(self, thumbnail_results):
        raise NotImplementedError("Must be implemented by subclass")

    def scroll_to_end(self):
        self.sleep()
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.sleep()
        self.click_show_more_button()
        self.sleep()

    def click_show_more_button(self):
        pass  # implemented in subclasses if relevant

    def sleep(self):
        time.sleep(
            self.sleep_between_interactions[0]
            + (self.sleep_between_interactions[1] - self.sleep_between_interactions[0])
            * random.random()
        )


class SearchGoogle(Search):
    def __init__(self, wd):
        super(SearchGoogle, self).__init__(wd)
        self.url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        # self.url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img&tbs=il:cl"  # creative commons license only

    def find_thumbnail_elements(self):
        return self.wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")

    def get_image_urls(self, thumbnail_results):
        img_urls = []
        for thumbnail in thumbnail_results:
            try:
                thumbnail.click()  # try to click thumbnail to get img src
                self.sleep()
            except Exception:
                continue

            images = self.wd.find_elements(By.CSS_SELECTOR, "img.r48jcc")
            for image in images:
                if image.get_attribute("src") and "http" in image.get_attribute("src"):
                    img_urls.append(image.get_attribute("src"))
        return img_urls

    def click_show_more_button(self):
        # <input jsaction="Pmjnye" class="mye4qd" type="button" value="Weitere Ergebnisse ansehen">
        show_more_btn = self.wd.find_elements(By.CLASS_NAME, "mye4qd")
        if (
            len(show_more_btn) == 1
            and show_more_btn[0].is_displayed()
            and show_more_btn[0].is_enabled()
        ):
            show_more_btn[0].click()


class SearchBing(Search):
    def __init__(self, wd):
        super(SearchBing, self).__init__(wd)
        # self.url = "https://www.bing.com/images/search?q={q}&form=QBLH&sp=-1&pq=c&sc=8-1&qs=n&first=1&scenario=ImageBasicHover"
        self.url = "https://www.bing.com/images/search?q={q}"

    def find_thumbnail_elements(self):
        # thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.mimg")
        return self.wd.find_elements(By.CLASS_NAME, "iusc")

    def get_image_urls(self, thumbnail_results):
        return [self.get_url_from_element_bing(img) for img in thumbnail_results]

    @staticmethod
    def get_url_from_element_bing(image_element):
        return json.loads(image_element.get_attribute("m"))["murl"]

    def click_show_more_button(self):
        show_more_btn = self.wd.find_elements(By.CLASS_NAME, "btn_seemore")
        if (
            len(show_more_btn) == 1
            and show_more_btn[0].is_displayed()
            and show_more_btn[0].is_enabled()
        ):
            show_more_btn[0].click()


class SearchBaidu(Search):
    def __init__(self, wd):
        super(SearchBaidu, self).__init__(wd)
        self.url = "https://image.baidu.com/search/index?tn=baiduimage&word={q}"

    def find_thumbnail_elements(self):
        return self.wd.find_elements(By.CLASS_NAME, "imgitem")

    def get_image_urls(self, thumbnail_results):
        return [img.get_attribute("data-objurl") for img in thumbnail_results]


class SearchYahoo(Search):
    def __init__(self, wd):
        super(SearchYahoo, self).__init__(wd)
        self.url = "https://images.search.yahoo.com/search/images;?fr2=sb-top-images.search&p={q}"

    def find_thumbnail_elements(self):
        return self.wd.find_elements(By.CSS_SELECTOR, "li>a>img")

    def get_image_urls(self, thumbnail_results):
        img_urls = []
        for thumbnail in thumbnail_results:
            # * Note: Apparently there is no more link to the full resolution image, thus, we can only save low-res
            img_url = urlparse(thumbnail.get_attribute("src"))
            query = parse_qs(img_url.query)
            query.pop("w", None)
            query.pop("h", None)
            img_url = img_url._replace(query=urlencode(query, True))
            img_urls.append(img_url.geturl())
        return img_urls

    def click_show_more_button(self):
        btn = retry(self.wd.find_elements, [By.NAME, "more-res"])
        if len(btn) == 1:
            btn[0].click()


def retry(fct, args, max_attempts=5):
    res = []
    retries = 0
    while retries < max_attempts:
        try:
            res = fct(*args)
            if isinstance(res, list):
                if len(res) > 0:
                    break
            else:
                break
        except:
            pass
        time.sleep(1.5)
        retries += 1
    return res
