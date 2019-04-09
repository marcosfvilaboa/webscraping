from scraper import MotorbikeScraper

output_file = "motorbike_accessories.csv"

scraper = MotorbikeScraper()
scraper.scrape_products()
scraper.data2csv(output_file)
print("\nSCRAPING PROCESS FINISHED!")

