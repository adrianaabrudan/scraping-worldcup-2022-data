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
        pages = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12]

        headers = []
        for th in driver.find_elements("xpath", '//*[@id="yw1"]/table/thead/tr/th'):
            headers.append(th.text)

        data.append(headers)

        for index, page in enumerate(pages):

            rows = driver.find_elements("xpath", '//*[@id="yw1"]/table/tbody/tr')
            rows_len = len(rows)

            columns = driver.find_elements("xpath", '//*[@id="yw1"]/table/thead/tr/th')
            columns_len = len(columns)

            for row in range(1, rows_len + 1):
                each_row = []
                for col in range(1, columns_len + 1):
                    if col in (3, 5):
                        element = driver.find_element("xpath", "//*[@id='yw1']/table/tbody/tr[" + str(
                            row) + "]/td[" + str(col) + "]//a[@title]")
                        each_row.append(element.get_attribute("title"))
                    elif col in (1, 4, 6):
                        element = driver.find_element("xpath", "//*[@id='yw1']/table/tbody/tr[" + str(
                            row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    elif col == 2:
                        element = driver.find_element("xpath", "//*[@id='yw1']/table/tbody/tr[" + str(row) + "]/td[" + str(
                                                            col) + "]").text
                        element = element.split('\n')[0]
                        each_row.append(element)

                data.append(each_row)

            next_page_index = index + 1

            if next_page_index < 10:
                sleep_time = random.randint(15, 25)
                next_page = driver.find_element("xpath", f'//*[@id="yw1"]/div[2]/ul/li[{pages[next_page_index]}]/a')
                driver.execute_script("arguments[0].click();", next_page)
                time.sleep(sleep_time)
            else:
                print("Data was scraped")

            pd = pandas.DataFrame(data)
            pd.to_csv("players_value.csv", index=False, header=False)
            yield {'row': data}

        driver.quit()


