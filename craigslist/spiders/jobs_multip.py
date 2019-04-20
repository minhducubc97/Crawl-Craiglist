# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class JobsMultipSpider(scrapy.Spider):
    name = 'jobs_multip'
    allowed_domains = ['newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        nodes = response.xpath('//p[@class="result-info"]')
        for node in nodes:
            title = node.xpath('a/text()').extract_first()
            address = node.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1] # remove the extra space and brackets
            yield{'Title': title, 'Address': address}

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        # initiate callback, setting dont_filter=True to allow accessing other domains
        yield Request(absolute_next_url, callback=self.parse, dont_filter=True)