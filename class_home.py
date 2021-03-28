from class_category import *


class Home:
    def __init__(self, site_url):
        self.url = site_url
        self.allcategories = []

        self.reponse = requests.get(site_url)
        self.soup = BeautifulSoup(self.reponse.text, "lxml")
        self.soup2 = self.soup.find("article", "product_page")

    def __get_category_urls(self):
        links = self.soup.find("div", "side_categories").ul.ul.find_all("li")
        for link in links:
            link = link.a.attrs["href"]
            finale_link = f"{site_url}/{link}"
            self.allcategories.append(finale_link)

    def run(self):
        self.__get_category_urls()
        for url_category in self.allcategories:
            category = Category(url_category)
            category.run()
            print(category)
