import csv

import scrapy
from scrapy.crawler import CrawlerProcess


dt = "2023-04-24"
URL = f"https://www.boxofficemojo.com/date/{dt}/"


class MySpider(scrapy.Spider):
    name = "boxofficemojo_spider"
    start_urls = [URL, ]

    def parse(self, response):
        listing = response.css("table.a-bordered.a-horizontal-stripes.a-size-base.a-span12.mojo-body-table.mojo-table-annotated.mojo-body-table-compact > tr")

        for each in listing:
            rank = each.css('td:first-child::text').get()
            rank_yesterday = each.css('td:nth-child(2)::text').get()
            release = each.css('td:nth-child(3) > a::text').get()

            daily = each.css('td:nth-child(4)::text').get()
            gross_change_day = each.css('td:nth-child(5)::text').get()
            gross_change_week = each.css('td:nth-child(6)::text').get()
            no_of_theaters = each.css('td:nth-child(7)::text').get()
            per_theaters_avg_gross = each.css('td:nth-child(8)::text').get()
            gross_to_date = each.css('td:nth-child(9)::text').get()
            no_of_days_in_release = each.css('td:nth-child(10)::text').get()
            distributor = each.css('td:nth-child(11) > a::text').get()

            print(
                rank,
                rank_yesterday,
                release,
                daily,
                gross_change_day,
                gross_change_week,
                no_of_theaters,
                per_theaters_avg_gross,
                gross_to_date,
                no_of_days_in_release,
                distributor,
                sep=" | "
            )

        # Write to CSV
        # YOUR CODE HERE
        header = [
            "rank",
            "rank_yesterday",
            "release",
            "daily",
            "gross_change_day",
            "gross_change_week",
            "no_of_theaters",
            "per_theaters_avg_gross",
            "gross_to_date",
            "no_of_days_in_release",
            "distributor",
        ]


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
