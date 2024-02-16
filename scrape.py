import requests
from bs4 import BeautifulSoup
import pandas as pd

Livres = []

URLcat = "https://books.toscrape.com/index.html"
pagecat = requests.get(URLcat)
soupcat = BeautifulSoup(pagecat.content, "html.parser")

# Rechercher les catégories
div_side_categorie = soupcat.find(class_="nav nav-list")
links = div_side_categorie.find_all("a")

# Stocker le nom des catgories dans une liste
# Stocker les liens des catégories dans une liste
urls = []
list_cat = []
for link in links:
    url = link.get("href")
    cat = link.text.strip()

    if url:
        list_cat.append(cat)
        urls.append(url)
# print(list_cat)
# print("\n")
# print(urls)

# Accéder au lien de la catégorie
for url in urls:
    if "books_1" in url:
        continue
    # print("\n")
    URL_EachCat = "https://books.toscrape.com/" + url
    # print(URL_EachCat)
    page_EachCat = requests.get(URL_EachCat)
    soup_EachCat = BeautifulSoup(page_EachCat.content, "html.parser")
    div_image_containers = soup_EachCat.find_all(class_="image_container")
    # print(div_image_containers)
    # print("\n")

    # Accéder au lien de chaque livre dans une catégorie
    for div_image_container in div_image_containers:
        href_EachCat = div_image_container.find("a")
        href_EachCat_text = (
            "https://books.toscrape.com/catalogue////" + href_EachCat.get("href")
        )
        # print(href_EachCat_text)

        # Accéder à la page de détails du livre
        page_each_book = requests.get(href_EachCat_text)
        soup_each_book = BeautifulSoup(page_each_book.content, "html.parser")

        # Extraire les informations du livre
        title = soup_each_book.find("h1").text.strip()
        price = soup_each_book.find(class_="price_color").text.strip()
        stock = soup_each_book.find(class_="instock availability").text.strip()
        description = (
            soup_each_book.find(id="content_inner").find_all("p")[3].text.strip()
        )

        # Imprimer et/ou Stocker les informations
        Livres.append(
            {
                "URL catégorie": URL_EachCat,
                "Titres": title,
                "Prix": price,
                "Stock": stock,
            }
        )
        print(Livres)
        # print("Titre:", title)
        # print("Prix:", price)
        # print("Stock:", stock)
        # print("Description:", description)
        # print("\n")

# Je crée une DataFrame
df = pd.DataFrame(Livres)
# J'envoie la DataFrame dans un CSV
df.to_csv("livres.csv", index=False, encoding="utf-8")



# 1er essai pour 1 livre :
# URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, "html.parser")
# # print(soup)

# title = soup.find("h1")
# prix = soup.find(class_= "price_color")
# stock = soup.find(class_= "instock availability")
# description = soup.find(id= "content_inner")
# descriptionp = description.find_all("p")[-1]
# print(title.text)
# print(prix.text)
# print(stock.text)
# print(descriptionp.text)


# div_href_EachCat = soup_EachCat.find(class_="image_container")
# href_EachCat = div_href_EachCat.find("a")
# # print(href_EachCat)
# href_EachCat_text = "https://books.toscrape.com/catalogue////" + href_EachCat.get("href")
# # print(href_EachCat_text)


# # je rentre dans chaque livre et j'extraie
# for livre in href_EachCat_text:
#     EachBook = requests.get(href_EachCat_text)
#     soup_EachBook = BeautifulSoup(page.content, "html.parser")
#     # print(soup_EachBook)
#     title = soup.find("h1")
#     prix = soup.find(class_= "price_color")
#     stock = soup.find(class_= "instock availability")
#     description = soup.find(id= "content_inner")
#     descriptionp = description.find_all("p")[-1]


# Extraire les données sur la page d'une catégorie (ex : crime) - a voir plus tard

# title_EachCat = soup_EachCat.find("h3" )
# title_text = title_EachCat.text.strip()
# div_EachCat= soup_EachCat.find(class_="product_price")
# price_EachCat = div_EachCat.find(class_="price_color")
# price_text = price_EachCat.text.strip()

# print(URL_EachCat)
# print(title_text)
# print(price_text)
