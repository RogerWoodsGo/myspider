# -*- coding: utf-8 -*-
import scrapy


class ExpampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["www.baidu.com"]
    start_urls = (
        'http://www.online.sh.cn/',
    )

    def parse(self, response):
        for sel in response.xpath('//body/'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print title, link, desc
            #        pass
