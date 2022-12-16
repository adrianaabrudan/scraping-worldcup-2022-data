import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
import time
import random
import pandas


class TheAnalystSpider(scrapy.Spider):
    name = 'transfermarkt'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.transfermarkt.com/2022-world-cup/marktwerte/pokalwettbewerb/WM22/pos//detailpos/0/altersklasse/alle',
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=r'./chromedriver')
        driver.get('https://www.transfermarkt.com/2022-world-cup/marktwerte/pokalwettbewerb/WM22/pos//detailpos/0/altersklasse/alle')
        time.sleep(random.randint(10, 20))

        data = []

        headers = []
        for th in driver.find_elements("xpath", '//*[@id="yw1"]/table/thead/tr/th'):
            headers.append(th.text)

        data.append(headers)

        rows = driver.find_elements("xpath", '//*[@id="yw1"]/table/tbody/tr[1]/td[2]/table/tbody/tr')
        rows_len = len(rows)

        columns = driver.find_elements("xpath", '//*[@id="yw1"]/table/thead/tr/th')
        columns_len = len(columns)

        for row in range(1, 3):
            each_row = []
            for col in range(1, columns_len + 1):
                if col in (3, 5):
                    element = driver.find_element("xpath", "//*[@id='yw1']/table/tbody/tr[" + str(
                        row) + "]/td[" + str(col) + "]//a[@title]")
                    each_row.append(element.get_attribute("title"))
                else:
                    element = driver.find_element("xpath", "//*[@id='yw1']/table/tbody/tr[" + str(
                        row) + "]/td[" + str(col) + "]").text
                    each_row.append(element)
            data.append(each_row)





