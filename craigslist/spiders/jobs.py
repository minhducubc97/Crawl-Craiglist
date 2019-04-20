# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        nodes = response.xpath('//p[@class="result-info"]')
        for node in nodes:
            # extract_first: extract the first matched element.
            title = node.xpath('a/text()').extract_first()
            address = node.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1] # remove the extra space and brackets
            relative_url = node.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield{'URL': absolute_url,'Title': title, 'Address': address}

