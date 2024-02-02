# Author: Léo Merkel
# GitHub: Orabis (https://github.com/Orabis)
# Purpose: For educational and instructional purposes only.
# This code is created for educational purposes and should not be used in real-world applications or real usage.
# In case of use, the author disclaims any responsibility for potential damages or any issues.

from utils.dl_img import pre_dl
from utils.http_request import get_all_albums

VERSION = "1.0.0"

initial_url = input("type the gallery url (https://www.flickr.com/PHOTOS/.../) \n:")
while not initial_url.startswith("https://www.flickr.com/photos/"):
    initial_url = input("incorrect link, retry (https://flickr.com/photos/...) \n:")
base_url = initial_url.strip()

initial_option = input(
    "type an option :\n 1 : download all imgs from the gallery \n 2 : retrieve albums, display and chose what to download \n"
)
while not initial_option.isdecimal():
    initial_option = input("incorrect value")


match int(initial_option):
    case 1:
        pre_dl(initial_url, base_url)
    case 2:
        albums = get_all_albums(initial_url, base_url)
        for album1, album2 in zip(albums[::2], albums[1::2]):
            print(
                f"id: {album1['id']: <3} name: {album1['title']: <15} | id: {album2['id']: <3} name: {album2['title']: <15}"
            )
        if len(albums) % 2 != 0:
            last_album = albums[-1]
            print(f"id: {last_album['id']: <3} name: {last_album['title']: <15}")
        try:
            albums_picked = [
                int(item)
                for item in input(
                    "Enter the list items (separated with space) :"
                ).split()
            ]
        except ValueError:
            raise ValueError("Give a number separated by spaces")
        links = [item["link"] for item in albums if item["id"] in albums_picked]
        pre_dl(links, base_url)

    case _:
        raise ValueError("unreachable option")
