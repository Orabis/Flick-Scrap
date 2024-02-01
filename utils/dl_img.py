import os
import re

from bs4 import BeautifulSoup
from utils.http_request import make_requests


def download_image(url, img_name):
    r = make_requests(url)

    if r.status_code == 200:
        folder = os.path.join("./output", img_name)

        with open(folder, "wb") as file:
            file.write(r.content)
        print(f"download done of {img_name}")
    else:
        print(f"Error during image download. Status code : {r.status_code}")


def pre_dl(initial_url, base_url):
    page_number = 1
    while True:
        index = initial_url.rfind('page')
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
        page_number = page_number + 1
        if soup.select_one(f'link[href="{base_url}page{page_number}/"][rel="next"]') is None:
            print("No images found stopping !")
            break
