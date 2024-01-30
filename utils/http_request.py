import requests
from bs4 import BeautifulSoup


def make_requests(initial_url):
    try:
        s = requests.Session()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        r = s.get(initial_url, headers={"User-Agent": user_agent})
        return r
    except requests.RequestException as e:
        print(f"{e} \n i guess you gave a wrong link")
        return None


def get_all_albums(initial_url):
    initial_url = initial_url + str("/albums/")
    r = make_requests(initial_url)
    soup = BeautifulSoup(r.content, "html.parser")
    for album in soup.find_all('a', attrs={'title': True}):
        print(album)
    return None

