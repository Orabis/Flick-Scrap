import time
import requests

import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver


def make_requests(initial_url):
    try:
        s = requests.Session()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        r = s.get(initial_url, headers={"User-Agent": user_agent})
        return r
    except requests.RequestException as e:
        print(f"{e} \n Error making the request")
        return None


def make_request_selenium(initial_url):
    try:
        browser = webdriver.Chrome()
        browser.get(initial_url)
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return browser
    except selenium.common.exceptions as e:
        (print(f"{e} \n Error making request with selenium"))


def get_all_albums(initial_url, base_url):
    albums = []
    iid = 1
    page_number = 1
    while True:
        index = initial_url.rfind("page")
        initial_url = initial_url + str("/albums")
        if index != -1:
            initial_url = initial_url[:index] + f"page{page_number}"
        else:
            initial_url = f"{initial_url}/page{page_number}"
        r = make_request_selenium(initial_url)
        soup = BeautifulSoup(r.page_source, "html.parser")
        for album in soup.find_all(
            lambda tag: tag.name == "a"
            and tag.get("href", "").startswith("/photos/")
            and tag.get("title")
        ):
            link = f"https://www.flickr.com{album.get('href')}"
            albums.append({"id": iid, "link": link, "title": album.get("title")})
            iid += 1
        if not albums:
            raise Exception("No albums found did you enter a correct link ?")
        page_number = page_number + 1
        soup_url = f'link[href="{base_url}/albums/page{page_number}/"][rel="next"]'
        if soup.select_one(soup_url) is None:
            break
    return albums
