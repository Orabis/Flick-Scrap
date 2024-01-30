from bs4 import BeautifulSoup
import re
from utils.dl_img import download_image
from utils.requests import make_requests

initial_url = input("type the gallery url (https://www.flickr.com/PHOTOS/.../) \n :")

initial_option = input(
    "type an option :\n 1 : download all img from the gallery \n 2 : retrieve albums, display and chose what to download \n"
)
while not initial_option.isdecimal():
    initial_option = input("incorrect value")


match int(initial_option):
    case 1:
        r = make_requests(initial_url)
        soup = BeautifulSoup(r.content, "html.parser")
        for link in soup.find_all("img"):
            cleaned_link = link.get("src")
            cleaned_link = cleaned_link.replace("//", "https://")
            img_name = re.search(r"/([^/]+\.jpg)$", cleaned_link).group(1)
            download_image(cleaned_link, img_name)
    case 2:
        print("2")
    case _:
        raise ValueError("unreachable option")
