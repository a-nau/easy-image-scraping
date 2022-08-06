# Copyright 2022 Fabian Bosler

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from selenium import webdriver

from src.scraping.search_engines import search_engine_factory


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver.Chrome, engine):
    wd.set_window_size(1920, 1080)
    search_engine = search_engine_factory(engine, wd)
    search_engine.load_search(query)

    thumbnail_results = []
    scroll_count = 0
    number_results = 0
    while len(thumbnail_results) < max_links_to_fetch:
        search_engine.scroll_to_end()
        thumbnail_results = search_engine.find_thumbnail_elements()
        if number_results == len(thumbnail_results):
            print("Scrolling did not find additional output, stopping search")
            break
        number_results = len(thumbnail_results)
        print("Found: {} image links. Continue ...".format(number_results))
        scroll_count += 1
    print(
        f"Found: {number_results} search results. Extracting first {max_links_to_fetch} links"
    )
    image_urls = search_engine.get_image_urls(thumbnail_results[:max_links_to_fetch])
    print(f"Found: {len(image_urls[:max_links_to_fetch])} image links, done!")
    return image_urls[:max_links_to_fetch]
