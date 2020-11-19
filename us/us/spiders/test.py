import scrapy
import logging


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'us.middlewares.RotateProxyMiddleware': 300,
            'us.middlewares.RotateAgentMiddleware': 301,
            'us.middlewares.SeleniumMiddleware': 302
        }
    }