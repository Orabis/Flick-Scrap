import os
import re

from bs4 import BeautifulSoup
from utils.http_request import make_requests, make_request_selenium


def download_image(url, img_name):
    r = make_requests(url)
    if r.status_code == 200:
        folder = os.path.join("./output", img_name)

        with open(folder, "wb") as file:
            file.write(r.content)
        print(f"download done of {img_name}")
    else:
        print(f"Error during image download. Status code : {r.status_code}")


def pre_dl(initial_urls, base_url):
    if isinstance(initial_urls, list):
        for initial_url in initial_urls:
            goto_album_and_dl(initial_url)
    else:
        while_dl(initial_urls, base_url, False)


def goto_album_and_dl(initial_url):
    r = make_request_selenium(initial_url)
    soup = BeautifulSoup(r.page_source, "html.parser")
    for link in soup.find_all(
        lambda tag: tag.name == "a"
        and tag.get("href", "").startswith("/photos/")
        and "overlay" in tag.get("class", [])
    ):
        link = f"https://www.flickr.com{link.get('href')}"
        while_dl(link, link, True)
    print("download end")


def while_dl(initial_url, base_url, come_from_list):
    page_number = 1
    while True:
        try:
            if not come_from_list:
                index = initial_url.rfind("page")
                if index != -1:
                    initial_url = initial_url[:index] + f"page{page_number}"
                else:
                    initial_url = f"{initial_url}/page{page_number}"
            print(f"making gallery {initial_url}")
            r = make_requests(initial_url)
            soup = BeautifulSoup(r.content, "html.parser")
            for link in soup.find_all("img"):
                cleaned_link = link.get("src")
                cleaned_link = cleaned_link.replace("//", "https://")
                img_name = re.search(r"/([^/]+\.jpg)$", cleaned_link).group(1)
                download_image(cleaned_link, img_name)
                if come_from_list:
                    break
            page_number = page_number + 1
            if (
                soup.select_one(
                    f'link[href="{base_url}/page{page_number}/"][rel="next"]'
                )
                is None
            ):
                print("No next page found !")
                break
        except AttributeError:
            raise Exception("No imgs found, abort")
