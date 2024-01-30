import os
from dotenv import load_dotenv
load_dotenv()
# Scrapy settings for FastBot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "FastBot"

SPIDER_MODULES = ["FastBot.spiders"]
NEWSPIDER_MODULE = "FastBot.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "FastBot (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'ERROR'

DNS_TIMEOUT = 600
DOWNLOAD_TIMEOUT = 20
# CLOSESPIDER_TIMEOUT = 5

REACTOR_THREADPOOL_MAXSIZE = 35

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100
CONCURRENT_ITEMS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
OXYLABS_ENABLED = os.getenv("OXYLABS_ENABLED", "False").lower() == "true"
OXYLABS_USER = os.getenv("OXYLABS_USER")
OXYLABS_PASSWORD = os.getenv("OXYLABS_PASSWORD")
OXYLABS_HOST = os.getenv("OXYLABS_HOST")
OXYLABS_PORT = os.getenv("OXYLABS_PORT")
#SPIDER_MIDDLEWARES = {
#    "FastBot.middlewares.FastbotSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # FastBot.middlewares.FastbotDownloaderMiddleware": 543
    "FastBot.middlewares.RotateUserAgentMiddleware": 400,
}

if OXYLABS_ENABLED:
    DOWNLOADER_MIDDLEWARES["FastBot.middlewares.RotateProxyMiddleware"] = 610
    DOWNLOADER_MIDDLEWARES["scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware"] = 110

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html

#EXTENSIONS = {
#    "scrapy.extensions.httpcache.HttpCache": 500,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "FastBot.pipelines.WebNotesPipeline": 1,
    "FastBot.pipelines.WebNotesErrorPipeline": 2,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.8
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY =3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 600
# HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
