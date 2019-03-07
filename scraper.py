import scrapy
import sys
from scrapy.crawler import CrawlerProcess
from w3lib.http import basic_auth_header


if len(sys.argv) == 1:
    sys.exit("X-CACHE-UPDATER is missing")

x_cache_updater_val = sys.argv[1]
x_depth = sys.argv[2]

print('X-CACHE-UPDATER value is ' + x_cache_updater_val)
print('DEPTH_LIMIT value is ' + x_depth)