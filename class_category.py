import requests
from bs4 import BeautifulSoup

from class_book import site_url, url_book, base_url_for_categories, Book


class Category:
    def __init__(self, category_url):
        self.url = category_url
        self.url_books = []

    def __scrape_book_urls(self, url_page):

        reponse = requests.get(url_page)
        books_urls = []
        if reponse.ok:

            soup = BeautifulSoup(reponse.text, "lxml")
            for h3 in soup.findAll("h3"):
                book_a = h3.find("a")
                book_url = book_a["href"]
                full_book_url = base_url_for_categories + "/".join(
                    book_url.split("/")[-2:]
                )
                books_urls.append(full_book_url)
        return books_urls

    def __get_all_urls_pages(self):
        """Return urls of pages in a category"""

        urls_pages = list()
        reponse = requests.get(self.url)
        soup = BeautifulSoup(reponse.text, "lxml")
        category_url_base = self.url
        urls_pages.append(category_url_base)
        nb = 2
        while soup.select(".next > a"):
            category_url = category_url_base.replace("index", f"page-{nb}")
            reponse = requests.get(category_url)
            soup = BeautifulSoup(reponse.text, "lxml")
            nb += 1
            urls_pages.append(category_url)
        return urls_pages

    def __all_urls_books_in_category(self):

        self.urls_books = []
        urls_pages = self.__get_all_urls_pages()
        for url_page in urls_pages:
            scrap = self.__scrape_book_urls(url_page)
            self.urls_books.extend(scrap)

    def run(self):
        self.__all_urls_books_in_category()
        for url_book in self.urls_books:
            book = Book(url_book)
            book.run()
            print(book)
