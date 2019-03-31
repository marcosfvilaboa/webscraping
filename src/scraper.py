import urllib3
import time
from bs4 import BeautifulSoup


class MotorbikeScraper():

    def __init__(self):
        self.url = "http://valtermotorstore.com"
        self.subdomain = "/catalog/seo_sitemap/category/"
        self.data = []

    def __download_html(self, url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data)
        return soup

    def scrape(self):
        print
        "Web Scraping of travels' crashes data from " + "'" + self.url + "'..."

        print
        "This process could take roughly 45 minutes.\n"

        # Start timer
        start_time = time.time()

        # Download HTML
        html = self.__download_html(self.url + self.subdomain)
        print
        "Downloading HTML..."
        bs = BeautifulSoup(html, 'html.parser')

    def data2csv(self, filename):
        # Overwrite to the specified file.
        # Create it if it does not exist.
        file = open("../csv/" + filename, "w+")

        # Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";");
            file.write("\n");