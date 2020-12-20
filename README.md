# Amazon Product Information Scraper
Implimentation of amazon product scraper using scrapy, with some analytics

## Initial Setup

```
pip install -r requirements.txt

```

## Scraping:

```
sh scrape.sh

```

* Add urls to url list in [amazon_scraper.py](https://github.com/Bearbobs/amazon-product-scraper/blob/main/amazon_scraper/spiders/amazon_scraper.py) 

* Alter number of pages to scrape in number_of_page variable 

 ## Analytics:
 
 ```
 sh analyse.sh
 
 ```
 
## ToDo Changes

* Create a seperate transformer function to modify raw data into directly usable format for analytics.

* Adding cli option in scrape.sh to scrape all pages with the help of per_page_result variable.(not implimented by default due to risk of getting blocked by amazon)

* Error Handling and unit tests

