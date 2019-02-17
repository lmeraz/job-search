# -*- coding: utf-8 -*-
from scrapy import Spider, Request
# from urllib.parse import SplitResult, urlencode, urlunsplit
from job_search.items import JobSearchItem


class IndeedSpider(Spider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = ['https://www.indeed.com/jobs?'
                  'as_and=python&as_phr=&as_any=aws&as_not=senior&as_ttl=&as_cmp=&jt=fulltime''&st='
                  '&sr=directhire&as_src=&salary=&radius=5&l=94109&fromage=any&limit=50&sort=date&psf=advsrch']

    def parse(self, response):
        links = response.xpath('//h2/a[@class="turnstileLink"]/@href').getall()

        for link in links:
            yield response.follow(link, callback=self.parse_job_offer)

        next_page = response.xpath('//span[@class="np"]/../../@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_offer(self, response):
        job = JobSearchItem()
        job['title'] = response.xpath('//h3').css('.jobsearch-JobInfoHeader-title::text').get()
        job['company'] = response.css('.jobsearch-InlineCompanyRating').xpath('./div/text()').get()
        job['company_rating'] = response.xpath('//meta[@itemprop="ratingValue"]/@content').get()
        job['company_reviews'] = response.css('.icl-Ratings-count::text').get()
        job['city'] = response.css('.jobsearch-InlineCompanyRating').xpath('./div[4]/text()').get()
        job['url'] = response.url
        job['description'] = ' '.join(response.css('.jobsearch-JobComponent-description ::text').getall())
        yield job
