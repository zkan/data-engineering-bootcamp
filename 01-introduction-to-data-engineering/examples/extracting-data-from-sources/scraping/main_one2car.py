import csv

import scrapy
from scrapy.crawler import CrawlerProcess


URL = "https://www.one2car.com/%E0%B8%A3%E0%B8%96%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%AD%E0%B8%87-%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A-%E0%B8%82%E0%B8%B2%E0%B8%A2"


class MySpider(scrapy.Spider):
    name = "one2car_spider"
    start_urls = [URL,]

    def parse(self, response):
        listing = response.css("article.listing")
        for each in listing:
            title = each.css("a.ellipsize::text").get().strip()
            url = each.css("a.ellipsize").attrib["href"]
            price = each.css("div.listing__price::text").get().strip()

            if not price:
                price = each.css("span.hot-deal__price span.weight--semibold::text").get()

            price = price.replace(",", "").replace(" บาท", "")
            print(title, url, price, sep=" | ")

        # Write to CSV
        # YOUR CODE HERE
        header = [
            "title",
            "url",
            "price",
        ]


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
