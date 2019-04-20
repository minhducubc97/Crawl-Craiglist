# -*- coding: utf-8 -*-
import scrapy


class TitlesSpider(scrapy.Spider):
    name = 'titles'
    allowed_domains = ['https://newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        # Use response.xpath to extract HTML nodes into titles
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        for title in titles:
            yield {'Title': title}
