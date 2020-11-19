# -*- coding: utf-8 -*-
import scrapy
import loguru
from datetime import date
from us.items import HistoryFile
import json
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy.exporters import CsvItemExporter
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary("/usr/bin/geckodriver")
from selenium.webdriver.support import expected_conditions as EC
import scrapy as sc
import re
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class StocksSpider(scrapy.Spider):
    name = 'chotot'
    allowed_domains = ["chotot.com"]
    start_urls = [
                'https://www.chotot.com/da-nang/mua-ban',
    ]
    base_url = 'https://www.chotot.com/da-nang/mua-ban'

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "us.middlewares.RotateProxyMiddleware": 300,
            "us.middlewares.RotateAgentMiddleware": 301,
            #"us.middlewares.NasdaqMiddleware": 302
        },
        "ITEM_PIPELINES": {
            "us.pipelines.NasdaqPipeline": 300
        }
    }

    def start_requests(self):
        urlRelative = 'https://www.chotot.com/da-nang/mua-ban?page=1'
        count = 0
        for page in range(1, 3):
            count = count + 1
            url = urlRelative + str(page)
            print(url)
            print('page - ', count)
            yield scrapy.Request(url, self.parse)

        # next_page = response.xpath("//div[@class='pagingItem___2g6n_']/a/@href").extract_first()
        # next_page_url = self.base_url + next_page
        # yield scrapy.Request(next_page_url, callback=self.parse)




    def parse(self, response):

        BROWSER_EXE = "/usr/lib/firefox/firefox.sh"
        GECKODRIVER = "/usr/bin/geckodriver"
        FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
        # webdriver setting
        PROFILE = webdriver.FirefoxProfile()

        PROFILE.set_preference("dom.webnotifications.enabled", False)
        PROFILE.set_preference("app.update.enabled", False)
        PROFILE.update_preferences()

        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_binary=FIREFOX_BINARY,
                                   firefox_profile=PROFILE)
        #frame_list = driver.find_element_by_xpath('//')
        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 5)
        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "w-660 d-ib va-top pos-rel")))
        for i in response.xpath("//div[@class='list-view']/div[@class='ListAds___3Mp16']/ul/div/li "):
            sanPham = i.xpath(".//a/div[2]/div/h3/text()").get()
            gia  = i.xpath(".//a/div[2]/div/div/span/span[@class='adPriceNormal___puYxd']/text()").get()
            nguoiBan  =  i.xpath(".//div[1]/div/div/a/div[2]/text() ").get()
            thoiGian  =i.xpath(".//div[1]/div/div/span[1]/text() ").get()
            diaDiem  = i.xpath(".//div[1]/div/div/span[2]/span/text()").get()
            yield {
                "Name ":sanPham,
                "Price ": gia ,
                "Saller ": nguoiBan,
                "Time ": thoiGian,
                "Location ":diaDiem,
            }
            # xem lai XPATH, loi XPATH cho chi
        pass












