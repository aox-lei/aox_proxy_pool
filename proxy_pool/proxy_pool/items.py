# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyPoolItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    city = scrapy.Field()
    http_type = scrapy.Field()
    country = scrapy.Field()