# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from dotenv import load_dotenv
import os
from .settings import OXYLABS_USER, OXYLABS_PASSWORD, OXYLABS_HOST, OXYLABS_PORT
import json
import requests
import random

from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent

load_dotenv()


class FastbotSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class FastbotDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RotateProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.username = OXYLABS_USER
        self.password = OXYLABS_PASSWORD
        self.host = OXYLABS_HOST
        self.port = OXYLABS_PORT

    def process_request(self, request, spider):

        # host = f'http://{self.username}:{self.password}@{self.host}:{self.port}'

        main_proxy_data = requests.get(self.host, auth=(self.username, self.password))
        main_proxy_data = json.loads(main_proxy_data.text)
        new_proxy_list = list()

        for proxy in main_proxy_data:
            new_proxy_list.append(f'{self.username}:{self.password}@{proxy["ip"]}:60000')

        ROTATING_PROXY_LIST = new_proxy_list

        proxy_host = random.choice(ROTATING_PROXY_LIST)

        request.meta['proxy'] = proxy_host

class RotateUserAgentMiddleware(object):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

        self.user_agent_list = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


    def process_request(self, request, spider):
        if self.user_agent_list:
            user_agent = self.user_agent_list.get_random_user_agent()
            request.headers.setdefault('User-Agent', user_agent)