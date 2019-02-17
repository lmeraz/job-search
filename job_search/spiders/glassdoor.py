# -*- coding: utf-8 -*-
import scrapy


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['http://glassdoor.com/']

    def parse(self, response):
        pass
