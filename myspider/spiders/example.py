# -*- coding: utf-8 -*-
import scrapy
import os
import codecs
import urlparse
from scrapy.http.request import Request
from pybloom import BloomFilter


class ExpampleSpider(scrapy.Spider):
    name = "example"
    url_bloom = BloomFilter(capacity = 100000,error_rate = 0.001)
    count = 0
    allowed_domains = ["www.online.sh.cn"]
    allowed_suffix = ["online.sh.cn"]
    start_urls = (
        'http://www.online.sh.cn/',
        #'http://eat.online.sh.cn/eat/gb/content/2015-09/02/content_7529978.htm',
    )

    def parse(self, response):
        self.count= self.count + 1
        print "excuted", self.count
        hsel = response.xpath('//body/*//a')
        page_list = []
#        href_content = []
        for sel in hsel:
            link = sel.xpath('@href').extract()
            if len(link) != 0:
                 url = self.parse_href(response, link[0])
                 if len(url) != 0 and url not in self.url_bloom:
                    yield Request(url=url, callback=self.parse, dont_filter=True)
                    self.url_bloom.add(url)
                    page_list.append(url)
            #content = sel.xpath('text()').extract()
            #href_content.extend(content)
        self.write_list_to_file('sub_urls.txt', page_list, 'ab')
        #self.write_file('url_content.txt', href_content)
        #def url_exist_judge(self, url):

    def parse_href(self, response, href):
        url = ""
        targeted = 0
        if href.startswith('http') or href.startswith('https'):
            url = str(href)
        elif href.startswith('/'):
            url = urlparse.urljoin(response.url, str(href))
        if(len(url) != 0):
            url_content = urlparse.urlparse(url)
            net_location = url_content.netloc
            for suffix in self.allowed_suffix:
                if net_location.endswith(suffix):
                    targeted = 1
                    print url.split(':')[1][2:]
                    #print response.body
                    if(url.split(':')[1][2:] != ""):
                        self.write_str_to_file(url.split(':')[1][2:], response.body.decode('utf-8'), 'wb')
                    break
        if(targeted != 1):
            url = ""
        return url

    def write_list_to_file(self, fn, list_content, mod):
        if not os.path.exists(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))
        try:
            with codecs.open(fn, mod, encoding='utf-8') as wcf:
                for tt in list_content:
                    wcf.write(tt)
                    wcf.write('\n')
        except:
            print "open file error"
    def write_str_to_file(self, fn, string, mod):
        if os.path.basename(fn) == '':
            fn = fn + "index.html"
        if not os.path.exists(os.path.dirname(fn)) and os.path.dirname(fn) != '':
            os.makedirs(os.path.dirname(fn))
        #try:
        with codecs.open(fn, mod, encoding='utf-8') as wcf:
                wcf.write(string)
        #except:
        #    print "open file error"
