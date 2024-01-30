from bs4 import BeautifulSoup
import requests

initial_url = input("rentrer l'url à la base :")

initial_option = input("rentrer l'option :\n 1 : récuperer toutes les images dans le site \n 2 : récuperer les albums dans la liste \n")
while not initial_option.isdecimal():
    initial_option = input("valeur incorrecte")
match int(initial_option):
    case 1:
        print("1")
    case 2:
        print("2")
    case _:
        raise ValueError(f"l'option est introuvable")
