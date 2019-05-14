import scrapy
import sys
import os
import pprint
import smtplib
from email.message import EmailMessage
from scrapy.crawler import CrawlerProcess
from w3lib.http import basic_auth_header
from scrapy import signals
import itertools
from datetime import timedelta



x_cache_updater_val = os.environ["X_CACHE_UPDATER"]
x_depth = os.environ["DEPTH"]
x_auth_username = os.environ["AUTH_USER"]
x_auth_password = os.environ["AUTH_PASSWORD"]
x_urls = os.environ["START_URLS"]
x_locale = os.environ["LOCALE"]
x_concurrent_requests_per_ip = os.environ["CONCURRENT_REQUESTS_PER_IP"]
x_closespider_timeout = os.environ["CLOSESPIDER_TIMEOUT"]
x_smtp_send_mail = int(os.environ["SEND_EMAIL"])
x_start_pages_only = os.environ["START_PAGES_ONLY"]
x_run_shop = os.environ["RUN_SHOP"]
x_debug_level = os.environ["DEBUG_LEVEL"]

print('X-CACHE-UPDATER value is ' + x_cache_updater_val)
print('DEPTH_LIMIT value is ' + x_depth)

x_urls_list = x_urls.split(',')
x_locale_list = x_locale.split(',')
x_start_urls = []
for i in x_urls_list:
    for j in x_locale_list:
          new = i + j
          x_start_urls.append(new)
print(x_start_urls)

class Scraper(scrapy.Spider):
    name = "Scraper"
    custom_settings = {
        'DEPTH_LIMIT': x_depth,
        "DEPTH_STATS_VERBOSE": "true",
        "CONCURRENT_REQUESTS_PER_IP": x_concurrent_requests_per_ip,
        "CLOSESPIDER_TIMEOUT": x_closespider_timeout,
        "LOG_LEVEL": x_debug_level,
    }
    start_urls = x_start_urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse(self, response):
        print('Processing page content for ' + response.url + '....')
        # run for sku or shop page
        if x_start_pages_only != "yes":
            print('RUN_SHOP:' + x_run_shop)
            if x_run_shop == "no":
                for next_page in response.xpath('//nav[@class="nav nav-products"]/ul/li/a/@href').extract():
                    yield response.follow(next_page, self.parse_category, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
            else:
                next_page = response.xpath('//nav[@class="nav nav-products"]/ul/li/a/@href').extract()
                yield response.follow(next_page[0], self.parse_category, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})



    # start sku page
    def parse_category (self, response):
        print('Processing category content for ' + response.url + '....')
        if x_run_shop == "no":
            for next_page in response.xpath('//ul[@class="row category-items-list"]/li/a/@href').extract():
                yield response.follow(next_page, self.parse_subcategory, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        else:
            next_page = response.xpath('//ul[@class="row category-items-list"]/li/a/@href').extract()
            yield response.follow(next_page[0], self.parse_shop_product_set, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})


    def parse_subcategory (self, response):
        print('Processing subcategory content for ' + response.url + '....')
        for next_page in response.xpath('//div[@class="shop-products"]/div/a/@href').extract():
           yield response.follow(next_page, self.parse_product, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        for next_page in response.xpath('//a[@class="icon-angle-right"]/@href').extract():
           print('Next Page:', next_page);
           yield response.follow(next_page, self.parse_subcategory, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_product (self, response):
        print('Processing product content for ' + response.url + '....')
        for next_page in response.xpath('//tr[@class="basic-info"]/td/a/@href').extract():
           yield response.follow(next_page, self.parse_item, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        for next_page in response.xpath('//a[@class="icon-angle-right"]/@href').extract():
           print('Next Page:', next_page);
           yield response.follow(next_page, self.parse_product, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_item (self, response):
        print('Processing item content for ' + response.url + '....')
    # end sku page

    # shop page
    def parse_shop_product_set(self, response):
        print('Processing shop page product set for ' + response.url + '....')
        product_set = []
        product_set.append(response.url.split("/")[-1])
        URL = response.url.rsplit("/", 1)[0]
        for next_page in response.xpath(
                '//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][1]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            products = next_page.split("/")[-1].replace(product_set[0], '')
            product_set.append(products.replace('_', ''))
        #print(product_set)
        #print('Product Set:', len(product_set))
        for subset in itertools.combinations(product_set, 1):
            #              URI = '_'.join(subset)
            URI = subset[0]
            full_url = URL + '/' + URI
            # print('Full URL:', full_url)
            yield response.follow(full_url, self.parse_shop_2, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(full_url, self.parse_shop_3, 'GET',
                                  headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_2 (self, response):
        print('Processing shop page level 2 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][2]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_3, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_4, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_3 (self, response):
        print('Processing shop page level 3 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][3]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_4, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_5, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_4 (self, response):
        print('Processing shop page level 4 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][4]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_5, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_6, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_5 (self, response):
        print('Processing shop page level 5 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][5]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_6, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_7, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_6 (self, response):
        print('Processing shop page level 6 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][6]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_7, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_8, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_7 (self, response):
        print('Processing shop page level 7 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][7]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_8, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_9, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_8 (self, response):
        print('Processing shop page level 8 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][8]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_9, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_10, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_9 (self, response):
        print('Processing shop page level 9 for ' + response.url + '....')
        for next_page in response.xpath('//div[contains(concat(" ",@class," "), " table-filter filter-panel js-filter-panel-shop ")][9]/div/ul[contains(concat(" ",@class," "), " filter-option-list ")]/li/a[contains(@href,"/s/")]/@href').extract():
            yield response.follow(next_page, self.parse_shop_10, 'GET',
                                headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})
        yield response.follow(response.url, self.parse_shop_10, 'GET',
                                 headers={'Authorization': basic_auth, 'X-CACHE-UPDATER': x_cache_updater_val})

    def parse_shop_10 (self, response):
        print('Processing shop page level 10 for ' + response.url + '....')

# end shop page

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Scraper, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('Finished')
        if x_smtp_send_mail:
            body = self.crawler.stats.get_stats()
            body = pprint.pformat(body)
            x_mailfrom = os.environ["MAILFROM"]
            x_smtp_host = os.environ["SMTP_HOST"]
            x_smtp_port = int(os.environ["SMTP_PORT"])
            x_smtp_to = os.environ["SMTP_TO"]
            x_smtp_subject = os.environ["SMTP_SUBJECT"]
            x_smtp_to_list = x_smtp_to.split(',')
            smtp_server = smtplib.SMTP(x_smtp_host, x_smtp_port)
            msg = EmailMessage()
            msg['Subject'] = x_smtp_subject
            msg['From'] = x_mailfrom
            msg['To'] = x_smtp_to_list
            msg.set_content(body)
            smtp_server.send_message(msg)
            smtp_server.quit()

basic_auth = basic_auth_header(x_auth_username, x_auth_password)

process = CrawlerProcess()
process.crawl(Scraper)
process.start()