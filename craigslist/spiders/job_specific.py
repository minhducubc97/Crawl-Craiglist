# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class JobSpecificSpider(scrapy.Spider):
    name = 'job_specific'
    allowed_domains = ['newyork.craigslist.org/search/egr/']
    start_urls = ['https://newyork.craigslist.org/search/egr//']

    def parse(self, response):
        nodes = response.xpath('//p[@class="result-info"]')
        for node in nodes:
            title = node.xpath('a/text()').extract_first()
            address = node.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = node.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            # meta: create a dictionary to prevent duplicate data
            yield Request(absolute_url, callback=self.parse_page, dont_filter=True, meta={'URL': absolute_url, 'Title': title,'Address': address})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = "https://newyork.craigslist.org" + relative_next_url

        yield Request(absolute_next_url, callback=self.parse)


    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        yield{'URL': url, 'Title': title, 'Address': address, 'Description': description}