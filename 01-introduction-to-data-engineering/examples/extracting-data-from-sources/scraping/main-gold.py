import csv

import scrapy
from scrapy.crawler import CrawlerProcess


URL = "https://ทองคําราคา.com/"


class MySpider(scrapy.Spider):
    name = "gold_price_spider"
    start_urls = [URL,]

    def parse(self, response):
        header = response.css("#divDaily h3::text").get().strip()
        print(header)
        table = response.css("#divDaily .pdtable")
        # print(table)
        # rows = table.xpath("//tr")
        rows = table.css("tr")
        # print(rows)
        for row in rows:
            print(row.css("td::text").extract())
            # print(row.xpath("td//text()").extract())


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
