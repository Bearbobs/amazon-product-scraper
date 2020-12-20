# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    total_results= scrapy.Field()
    title = scrapy.Field()
    asin = scrapy.Field()
    total_rating = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    selling_rank = scrapy.Field()
    node_id = scrapy.Field()
    node_rank = scrapy.Field()
    
