# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json

import scrapy
from scrapy import signals
from selenium import webdriver
import time
import random
import loguru
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait

binary = FirefoxBinary("/usr/bin/geckodriver")






class RotateAgentMiddleware(object):

    def process_request(self, request, spider):
        BROWSER_EXE = "/usr/lib/firefox/firefox.sh"
        GECKODRIVER = "/usr/bin/geckodriver"
        FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
        # webdriver setting
        PROFILE = webdriver.FirefoxProfile()

        PROFILE.set_preference("dom.webnotifications.enabled", False)
        PROFILE.set_preference("app.update.enabled", False)

        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_binary=FIREFOX_BINARY,
                                   firefox_profile=PROFILE
                                   )

        # webdriver request
        # driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://deviceatlas.com/blog/list-of-user-agent-strings")
        time.sleep(1)

        # real time random select user agent from website
        agent_list = driver.find_elements_by_xpath("//td")
        agent = (random.choice(agent_list)).text
        loguru.logger.info("Hold Agent {agent}".format(agent=agent))
        driver.quit()

        # hold user agent
        request.headers["User-Agent"] = agent
class RotateProxyMiddleware(object):

    def process_request(self, request, spider):
        BROWSER_EXE = "/usr/lib/firefox/firefox.sh"
        GECKODRIVER = "/usr/bin/geckodriver"
        FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
        # webdriver setting
        PROFILE = webdriver.FirefoxProfile()

        PROFILE.set_preference("dom.webnotifications.enabled", False)
        PROFILE.set_preference("app.update.enabled", False)

        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_binary=FIREFOX_BINARY,
                                   firefox_profile=PROFILE
                                   )

        # webdriver request
        # driver = webdriver.Chrome(chrome_options=options)
        # driver.get("http://free-proxy-list.net")
        # time.sleep(1)
        #
        # # real time random select free proxy from website
        # row = int(random.randint(1, 20))
        # ip = driver.find_element_by_xpath("//tbody/tr[{row}]/td[1]".format(row=row)).text
        # port = driver.find_element_by_xpath("//tbody/tr[{row}]/td[2]".format(row=row)).text
        # proxy = "{ip}:{port}".format(ip=ip, port=port)
        # loguru.logger.info("Hold Proxy {proxy}".format(proxy=proxy))
        driver.quit()

        # hold proxy
        # request.meta["proxy"] = proxy


# class NasdaqMiddleware(object):
#
#     def process_request(self, request, spider):
#         data = []
#         url = request.url
#
#         BROWSER_EXE = "/usr/lib/firefox/firefox.sh"
#         GECKODRIVER = "/usr/bin/geckodriver"
#         FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
#         # webdriver setting
#         PROFILE = webdriver.FirefoxProfile()
#
#         PROFILE.set_preference("dom.webnotifications.enabled", False)
#         PROFILE.set_preference("app.update.enabled", False)
#         PROFILE.update_preferences()
#
#         driver = webdriver.Firefox(executable_path=GECKODRIVER,
#                                    firefox_binary=FIREFOX_BINARY,
#                                    firefox_profile=PROFILE)
#
#         driver.set_window_size(1440, 800)
#         driver.delete_all_cookies()
#         driver.get(url)
#
#         # clean popup
#         popup_xpath = (
#             ".//button["
#             "contains(@class, \"agree-button\")"
#             " and "
#             "contains(@class, \"eu-cookie-compliance-default-button\")"
#             "]"
#         )
#         popup_element = WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable((By.XPATH, popup_xpath))
#         )
#         loguru.logger.warning(popup_element)
#         popup_element.click()
#         time.sleep(5)
#
#         # select time
#         time_xpath = (
#             ".//div["
#             "@class=\"table-tabs__list\""
#             "]/button[5]"
#         )
#         time_element = WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable((By.XPATH, time_xpath))
#         )
#         time_element.click()
#         time.sleep(5)
#
#         # page count
#         count_xpath = (
#             ".//div["
#             "@class=\"pagination__pages\""
#             "]/button[8]"
#         )
#         count = driver.find_element_by_xpath(count_xpath).text
#         loguru.logger.info("Totally {count} pages".format(count=count))
#
#         next_xpath = ".//button[@class=\"pagination__next\"]"
#         for i in range(int(count)):
#             next_element = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, next_xpath))
#             )
#             data.append(driver.page_source)
#             next_element.click()
#             time.sleep(3)
#
#         driver.quit()
#
#         return scrapy.http.HtmlResponse(url=url,
#                                         status=200,
#                                         body=json.dumps(data).encode('utf-8'),
#                                         encoding='utf-8')
class UsDownloaderMiddleware(object):
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
        spider.logger.info('Spider opened: %s' % spider.name)




