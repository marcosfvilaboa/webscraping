from scraper import MotorbikeScraper

output_file = "dataset.csv"

scraper = MotorbikeScraper()
scraper.scrape_products()
scraper.data2csv(output_file)
print("\n\n SCRAPING PROCESS FINISHED!")
