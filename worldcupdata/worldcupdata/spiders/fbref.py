import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
import time
import random
import pandas


class TheAnalystSpider(scrapy.Spider):
    name = 'fbref'
    # allowed_domains = ['www.https://fbref.com']
    # start_urls = ['https://fbref.com/en/comps/1/stats/World-Cup-Stats']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://fbref.com/en/comps/1/stats/World-Cup-Stats',
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=r'./chromedriver')
        driver.get('https://fbref.com/en/comps/1/stats/World-Cup-Stats')
        time.sleep(random.randint(5, 10))

        data = []

        headers = []
        for th in driver.find_elements("xpath", '//*[@id="stats_standard"]/thead/tr[2]/th'):
            headers.append(th.text)
        data.append(headers[1:])

        # print(data)

        rows = driver.find_elements("xpath", '//*[@id="stats_standard"]/tbody/tr')
        rows_len = len(rows) + 1

        columns = driver.find_elements("xpath", '//*[@id="stats_standard"]/thead/tr[2]/th')
        columns_len = len(columns)

        rows_list = [i for i in range(1, rows_len) if i % 26 != 0]

        for row in rows_list:
            each_row = []
            for col in range(1, columns_len):
                element = driver.find_element("xpath", '//*[@id="stats_standard"]/tbody/tr[' + str(
                    row) + ']/td[' + str(col) + ']').text
                each_row.append(element)
            data.append(each_row)
        # print(data)

        pd = pandas.DataFrame(data)
        pd.to_csv("fbref.csv", index=False, header=False)
        yield {'row': data}

        driver.quit()
