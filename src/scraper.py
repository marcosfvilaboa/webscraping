from urllib import robotparser
from bs4 import BeautifulSoup
import pandas as pd
import os
import atexit
import urllib3
import time


class MotorbikeScraper:

    def __init__(self):
        """
        Constructor of the class
        """
        self.url = "https://valtermotostore.com"
        self.subdomain = "/catalog/seo_sitemap/category/?p=1"
        self.data = pd.DataFrame()
        self.delay = 0

    @staticmethod
    def __download_html(url):
        """
        Method to create a BeautifulSoup object from given url

        :param url: url origin address
        :return: soup
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager(maxsize=10)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5 37.36 (KHTML, like Gecko) "
                          "Chrome/56.0.2924.87 Safari/537.36"
        }
        response = http.request('GET', url, headers=headers)
        soup = BeautifulSoup(response.data, "html.parser")
        return soup

    # @staticmethod
    def parse_robots_txt(self):
        rp = robotparser.RobotFileParser()
        rp.set_url(self.url + '/robots.txt')
        rp.read()
        user_agent = '*'
        self.delay = rp.crawl_delay("*")
        print("The delay in robots.txt is", self.delay)
        print("ATTENTION: The process could take several hours!")
        if rp.can_fetch(user_agent, self.url) is False:
            print("User-agent isn't allowed by robots.txt")
            atexit()
        else:
            print("User-agent is allowed by robots.txt")


    def scrape_categories(self):
        """
        Method to scrap the categories of the fixed url from constructor.
        It constructs a new dataframe named categories_df

        :return: categories_df
        """
        html = self.__download_html(self.url + self.subdomain)
        categories = []
        next_page = True
        while next_page:
            for ul in html.findAll("ul", class_="sitemap"):
                for c in ul.findAll("li", class_="level-1"):
                    category_object = c.find("a")
                    category_motorbike = c.find_previous_sibling("li", class_="level-0").text
                    category_name = category_object.text
                    category_link = category_object['href']
                    categories.append((category_motorbike, category_name, category_link))

            next_page_object = html.find("a", class_="next i-next")
            if next_page_object is not None:
                html = self.__download_html(next_page_object['href'])
            else:
                next_page = False
            time.sleep(self.delay)
        categories_df = pd.DataFrame(categories, columns=["category_motorbike", "category_name", "category_link"])
        return categories_df

    def scrape_products(self):
        """
        Method to scrap all the urls of the categories (call to scrape_products function) and
        every page of every category.
        It constructs a dataframe to the field self.data
        """
        print("\nWeb Scraping of High-Tech Parts for Race Bikes data from ", "'", self.url, "'...")
        # Start timer
        start_time = time.time()
        print("Starting process at ", time.ctime(start_time))

        # parse robots.txt to find if user-agent = * can fetch
        self.parse_robots_txt()

        # Download categories
        print("Downloading categories...")
        categories = self.scrape_categories()

        print(categories.__len__(), " categories saved!")
        print("Downloading HTML of every category")
        products = []
        # Scrap url of every category
        for index, c in categories.iterrows():
            category_motorbike = c['category_motorbike']
            category_name = c['category_name']
            url = c['category_link']
            html = self.__download_html(url)
            product_list = html.find("ol", class_="products-list")
            if product_list is not None:
                for p in product_list.findAll("li", class_="item", recursive=False):
                    product_title = p.find(class_="product-name").text
                    product_sku = p.find(id="sku").text.replace("Code: ", "")
                    product_price = p.find(class_="price").text.replace("€", "")
                    product_image = p.find("img")['src']
                    products.append((category_motorbike, category_name, product_sku, product_title, product_price,
                                     product_image))
            time.sleep(self.delay)

        print("HTML downloading finished!")
        self.data = pd.DataFrame(products, columns=["category_motorbike", "category_name", "product_sku",
                                                    "product_title", "product_price",
                                                    "product_image"])

        # Stop timer
        stop_time = time.time()
        print("Process stopped at ", time.ctime(stop_time))
        total_time = stop_time - start_time
        print("Lasted ", int(total_time / 60), "minutes")
        print(self.data)

    def data2csv(self, filename):
        """
        Method to create a CSV file from dataframe in field self.data
        It constructs a file in a csv folder with pandas
        :param filename: name of the file to write in
        """
        root = '../csv'
        if not os.path.exists(root):
            os.mkdir(root)

        fullname = os.path.join(root, filename)

        self.data.to_csv(fullname, index_label='row')
