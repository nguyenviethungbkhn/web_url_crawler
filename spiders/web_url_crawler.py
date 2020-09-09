import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
from ..items import WebUrlItem
import sys
import pandas as pd
from twisted.internet.error import ConnectionLost, TCPTimedOutError, TimeoutError

class WebUrlCrawler(CrawlSpider):
    name = "web_url_crawler"
    # allowed_domains = [""]
    start_urls = []

    def __init__(self, *a, **kw):
        super(WebUrlCrawler, self).__init__(*a, **kw)
        df = pd.read_csv('web_url_crawler/data/gg_search_lang.csv')
        self.start_urls = list(set(df["url"].tolist()))
        # print(self.start_urls)
    
    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        if 'http' not in url:
            url = 'https://' + url
        return Request(url, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)
    
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("aaaa")
        if failure.check(ConnectionLost, TCPTimedOutError, TimeoutError):
            url = url.replace("https", "http")
            return Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = WebUrlItem()
        item["url"] = response.url
        item["web_title"] = response.xpath("//head/title/text()").extract_first()
        yield item
