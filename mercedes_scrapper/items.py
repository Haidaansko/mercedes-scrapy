# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MercedesScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    cars = scrapy.Field()


class CarItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    engine = scrapy.Field()
    inner = scrapy.Field()
    price = scrapy.Field()
    start = scrapy.Field()
    monthly = scrapy.Field()
    special = scrapy.Field()