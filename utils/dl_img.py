import os
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
