import scrapy
import sys
import os
from scrapy.crawler import CrawlerProcess
from w3lib.http import basic_auth_header



x_cache_updater_val = os.environ["X-CACHE-UPDATER"]
x_depth = os.environ["DEPTH"]
x_auth_username = os.environ["AUTH_USER"]
x_auth_password = os.environ["AUTH_PASSWORD"]
x_start_urls = os.environ["START_URLS"]
x_concurrent_requests_per_ip = os.environ["CONCURRENT_REQUESTS_PER_IP"]
x_closespider_timeout = os.environ["CLOSESPIDER_TIMEOUT"]

print('X-CACHE-UPDATER value is ' + x_cache_updater_val)
print('DEPTH_LIMIT value is ' + x_depth)



class Scraper(scrapy.Spider):
    name = "Scraper"
    custom_settings = {
        'DEPTH_LIMIT': x_depth,
        "DEPTH_STATS_VERBOSE": "true",
        "CONCURRENT_REQUESTS_PER_IP": x_concurrent_requests_per_ip,
        "CLOSESPIDER_TIMEOUT": x_closespider_timeout,
    }
    start_urls = [
        x_start_urls,
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse(self, response):
        print('Processing page content for ' + response.url + '....')

        for next_page in response.css('.nav-products a'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.facet-input-class-anchor'):
            yield response.follow(next_page, self.parse, 'GET',
                          headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.tealium-clickOnProduct'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.product-thumb'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.megamenu-list-lnk'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.product-wrapper > a'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        for next_page in response.css('.tealium-skuLinkPgroup'):
            yield response.follow(next_page, self.parse, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

        print('Done processing page content for ' + response.url + '.')


basic_auth = basic_auth_header(x_auth_username, x_auth_password)

process = CrawlerProcess()
process.crawl(Scraper)
process.start()