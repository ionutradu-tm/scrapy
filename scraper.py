import scrapy
import sys
import os
from scrapy.crawler import CrawlerProcess
from w3lib.http import basic_auth_header



x_cache_updater_val = os.environ["X-CACHE-UPDATER"]
x_depth = os.environ["DEPTH"]

print('X-CACHE-UPDATER value is ' + x_cache_updater_val)
print('DEPTH_LIMIT value is ' + x_depth)