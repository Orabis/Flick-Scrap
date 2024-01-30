from bs4 import BeautifulSoup
import re
from utils.dl_img import download_image
from utils.http_request import make_requests

initial_url = input("type the gallery url (https://www.flickr.com/PHOTOS/.../) \n :")
base_url = initial_url.strip()

initial_option = input(
    "type an option :\n 1 : download all img from the gallery \n 2 : retrieve albums, display and chose what to download \n"
)
while not initial_option.isdecimal():
    initial_option = input("incorrect value")

page_number = 1

match int(initial_option):
    case 1:
        while True:
            index = initial_url.rfind('page')
            if index != -1:
                initial_url = initial_url[:index] + f"page{page_number}"
            else:
                initial_url = f"{initial_url}page{page_number}"
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
    case 2:
        print("2")
    case _:
        raise ValueError("unreachable option")
