import scrapy
import re
from bs4 import BeautifulSoup as BS
from ..items import Product


class AmazonScraper(scrapy.Spider):
    name = "amazon_scraper"

    # How many pages you want to scrape
    no_of_pages = 1

    total_results = 0

    # per_page_result can be used to scrape all results, but it should be avoided as may result in ip block
    # no_of_page=total_results // per_page_result
    per_page_result= 0

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.amazon.in/s?k=mobile&ref=nb_sb_noss_2"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):

        self.no_of_pages -= 1

        soup = BS(response.text, features="lxml")
        refined_soup = BS(str(soup.findAll("div", {
                          "class": "a-section a-spacing-small a-spacing-top-small"})), features="lxml")
        self.total_results = re.search(
            r'over(.*?)results', refined_soup.select_one("span").text).group(1).strip()
        self.per_page_result = re.search(
            r'-(.*?)of', refined_soup.select_one("span").text).group(1).strip()
        products = response.xpath(
            "//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()

        for product in products:
            final_url = response.urljoin(product)
            yield scrapy.Request(url=final_url, callback=self.parse_product, headers=self.headers)

        if(self.no_of_pages > 0):
            next_page_url = response.xpath(
                "//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=final_url, callback=self.parse, headers=self.headers)

    def parse_product(self, response):
        title = response.xpath("//span[@id='productTitle']//text()").get(
        ) or response.xpath("//h1[@id='title']//text()").get()
        if title != None:
            title=title.strip()


        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath(
            "//span[@class='a-icon-alt']//text()").get()
        total_rating = response.xpath(
            "//span[@id='acrCustomerReviewText']//text()").get()
        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath(
            "//span[@id='priceblock_dealprice']//text()")
        if len(price) > 1:
            price = price[1].get()
        elif len(price) == 1:
            price = price[0].get()
        else:
            price = price.get()

        asin = response.xpath(
            "//table[@id='productDetails_detailBullets_sections1']//td//text()").get()
        try:
            selling_rank = response.xpath(
                "//table[@id='productDetails_detailBullets_sections1']//tr//td//span").getall()[-2:-1][0]
            selling_rank_clean = re.search(
                r'#(.*?)[(\[]', selling_rank).group(1).strip()
        except IndexError:
            selling_rank_clean=""
        try:
            node = response.xpath(
                "//table[@id='productDetails_detailBullets_sections1']//tr//td//span").getall()[-1:][0]
            node_id = re.search(r'href=[\'"]?([^\'" >]+)',
                                node).group(1).split("/")[4]
            node_rank = re.search(r'#(.*?)in', node).group(1)
        except IndexError:
            node_id=""
            node_rank=""

        yield Product(total_results=self.total_results, title=title, asin=asin, total_rating=total_rating, rating=rating, price=price,node_id=node_id, node_rank=node_rank, selling_rank=selling_rank_clean)
