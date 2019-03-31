from scraper import TravelScraper

output_file = "dataset.csv"

scraper = MotorbikeScraper();
scraper.scrape();
scraper.data2csv(output_file);