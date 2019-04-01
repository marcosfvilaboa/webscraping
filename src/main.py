from scraper import MotorbikeScraper

output_file = "dataset.csv"

scraper = MotorbikeScraper()
scraper.scrapeProducts()
# scraper.data2csv(output_file)
