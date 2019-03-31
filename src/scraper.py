import urllib3
import time
from bs4 import BeautifulSoup


class MotorbikeScraper():

    def __init__(self):
        self.url = "https://valtermotostore.com"
        self.subdomain = "/catalog/seo_sitemap/category/"
        self.data = []

    def __download_html(self, url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager(maxsize=10)
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "html.parser")
        return soup

    def scrape(self):
        print("Web Scraping of travels' crashes data from ", "'", self.url, "'...\n")

        print("This process could take roughly 45 minutes.\n")

        # Start timer
        start_time = time.time()
        print("Starting process at ", time.ctime(start_time), "...\n")

        # Download HTML
        print("Downloading HTML...\n")
        html = self.__download_html(self.url + self.subdomain)

        for ul in html.findAll("ul", class_="sitemap"):
            for a in ul.findAll("a", href=True):
                print(a.text)

    def data2csv(self, filename):
        # Overwrite to the specified file.
        # Create it if it does not exist.
        file = open("../csv/" + filename, "w+")

        # Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";");
            file.write("\n");