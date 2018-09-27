# -*- coding: utf-8 -*-
import scrapy


class IhuanSpider(scrapy.Spider):
    name = 'ihuan'
    allowed_domains = ['ip.ihuan.me']

    def parse(self, response):
        pass

    def start_requests(self):
        yield scrapy.Request('https://ip.ihuan.me/')
