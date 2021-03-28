import requests
from bs4 import BeautifulSoup

site_url = "http://books.toscrape.com"

url_book = "https://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"

base_url_for_categories = "https://books.toscrape.com/catalogue/"


class Book:
    def __init__(self, url_book):
        self.url = url_book
        self.title = ""
        self.category = ""
        self.rating = ""
        self.img_url = ""
        self.description = ""

        reponse = requests.get(url_book)
        self.soup = BeautifulSoup(reponse.text, "lxml")
        self.soup2 = self.soup.find("article", "product_page")

    def __get_title(self):
        self.title = (
            self.soup.find("title").get_text().strip().strip("\n").split("|")[0]
        )

    def __get_category(self):
        links = self.soup.findAll("a")

        for u in links:
            if "category" in u["href"] and u.text != "Books":
                self.category = u.text
                break

    def __get_rating(self):
        ps = self.soup.find_all("p")
        p_rating = None

        for p in ps:
            if "star-rating" in p["class"]:
                p_rating = p["class"]
                break
        assert p_rating is not None
        letters_to_numbers = {
            "Zero": 0,
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }
        self.rating = letters_to_numbers[p_rating[1]]

    def __get_image(self):
        try:
            self.img_url = self.soup2.find("img")
            self.img_url = (site_url + self.soup2.img["src"]).replace("../..", "")
        except AttributeError:
            print("The book don't have an image")

    def __get_description(self):
        try:
            self.description = self.soup2.find("p", recursive=False)
        except AttributeError:
            return str("Il n'y a pas de description.")

    def run(self):
        self.__get_title()
        self.__get_category()
        self.__get_rating()
        self.__get_image()
        self.__get_description()

    def __str__(self):
        output = f"url : {self.url}\ntitle : {self.title}\ncategory : {self.category}\nrating : {self.rating}\nimage : {self.img_url}\ndescription : {self.description}"
        return output
