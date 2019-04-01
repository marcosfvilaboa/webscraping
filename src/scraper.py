import urllib3
import time
from bs4 import BeautifulSoup
import pandas as pd


class MotorbikeScraper():

    def __init__(self):
        self.url = "https://valtermotostore.com"
        self.subdomain = "/catalog/seo_sitemap/category/?p=1"
        self.data = []

    def __download_html(self, url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager(maxsize=10)
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "html.parser")
        return soup

    def scrapeCategories(self):
        print("Web Scraping of travels' crashes data from ", "'", self.url, "'...\n")

        print("This process could take roughly 45 minutes.\n")

        # Start timer
        start_time = time.time()
        print("Starting process at ", time.ctime(start_time), "...\n")

        # Download HTML
        print("Downloading HTML...\n")

        html = self.__download_html(self.url + self.subdomain)
        categories = []
        nextPage = True
        while(nextPage == True):
            for ul in html.findAll("ul", class_="sitemap"):
                for c in ul.findAll("li", class_="level-1"):
                    categoryObject = c.find("a")
                    categoryMotorbike = c.find_previous_sibling("li", class_="level-0").text
                    categoryName = categoryObject.text
                    categoryLink = categoryObject['href']
                    categories.append((categoryMotorbike, categoryName, categoryLink))

            nextPageObject = html.find("a", class_="next i-next")
            if(nextPageObject is not None):
                html = self.__download_html(nextPageObject['href'])
                print(nextPageObject['href'])
            else:
                nextPage = False

        categories_df = pd.DataFrame(categories, columns=["categoryMotorbike", "categoryName", "categoryLink"])
        return categories_df

    def scrapeProducts(self):

        categories = self.scrapeCategories()

        products = []

        for index, c in categories.iterrows():

            categoryMotorbike = c['categoryMotorbike']
            categoryName = c['categoryName']
            url = c['categoryLink']
            html = self.__download_html(url)
            productList = html.find("ol", class_="products-list")
            if(productList is not None):
                for p in productList.findAll("li" , class_="item", recursive=False):
                    productTitle = p.find(class_="product-name").text
                    productSKU = p.find(id="sku").text
                    productDescription = p.find(class_="desc").text
                    productImage = p.find("img")['src']

                    products.append((categoryMotorbike,categoryName,productSKU, productTitle, productDescription, productImage))

        products_df = pd.DataFrame(products, columns=["categoryMotorbike","categoryName","productSKU", "productTitle", "productDescription", "productImage"])
        return products_df


    def data2csv(self, filename):
        # Overwrite to the specified file.
        # Create it if it does not exist.
        file = open("../csv/" + filename, "w+")

        # Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";");
            file.write("\n");

