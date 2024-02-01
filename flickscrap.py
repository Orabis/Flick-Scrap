from utils.dl_img import pre_dl
from utils.http_request import get_all_albums

initial_url = input("type the gallery url (https://www.flickr.com/PHOTOS/.../) \n :")
base_url = initial_url.strip()

initial_option = input(
    "type an option :\n 1 : download all img from the gallery \n 2 : retrieve albums, display and chose what to download \n"
)
while not initial_option.isdecimal():
    initial_option = input("incorrect value")


match int(initial_option):
    case 1:
        pre_dl(initial_url, base_url)
    case 2:
        albums = get_all_albums(initial_url)
        for album in albums:
            print(f"id: {album['id']} name: {album['title']}")
        albums_picked = [int(item) for item in input("Enter the list items (separated with space)").split()]
    case _:
        raise ValueError("unreachable option")
