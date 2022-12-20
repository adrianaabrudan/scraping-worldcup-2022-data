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
        time.sleep(random.randint(5, 7))

        tags = ["stats_standard", "stats_squads_standard_for"]

        for tag in tags:
            data = []

            headers = []
            for th in driver.find_elements("xpath", f'//*[@id="{tag}"]/thead/tr[2]/th'):
                headers.append(th.text)

            data.append(headers)

            rows = driver.find_elements("xpath", f'//*[@id="{tag}"]/tbody/tr')
            rows_len = len(rows) + 1

            columns = driver.find_elements("xpath", f'//*[@id="{tag}"]/thead/tr[2]/th')
            columns_len = len(columns)

            rows_list = []
            if tag == "stats_standard":
                rows_list = [i for i in range(1, rows_len) if i % 26 != 0]
            elif tag == "stats_squads_standard_for":
                rows_list = [i for i in range(1, rows_len) if i % 26 != 0 and i % 27 != 0]

            for row in rows_list:
                each_row = []
                for col in range(1, columns_len):
                    if col == 1:
                        element = driver.find_element("xpath", f'//*[@id="{tag}"]/tbody/tr[' + str(row) + ']/th[1]').text
                        each_row.append(element)
                        element = driver.find_element("xpath", f'//*[@id="{tag}"]/tbody/tr[' + str(row) + ']/td[' + str(col) + ']').text
                        each_row.append(element)
                    else:
                        element = driver.find_element("xpath", f'//*[@id="{tag}"]/tbody/tr[' + str(
                            row) + ']/td[' + str(col) + ']').text
                        each_row.append(element)
                data.append(each_row)
                # print(data)

            pd = pandas.DataFrame(data)
            if tag == "stats_standard":
                pd.to_csv("fbref_files/fbref_players.csv", index=False, header=False)
            elif tag == "stats_squads_standard_for":
                pd.to_csv("fbref_files/fbref_teams.csv", index=False, header=False)
            yield {'row': data}

        driver.quit()
