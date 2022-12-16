import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
import time
import random
import pandas


class TheAnalystSpider(scrapy.Spider):
    name = 'theanalyst'
    # allowed_domains = ['www.dataviz.theanalyst.com']
    # start_urls = ['https://dataviz.theanalyst.com/fifa-world-cup-2022/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://dataviz.theanalyst.com/fifa-world-cup-2022/',
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=r'./chromedriver')
        driver.get('https://dataviz.theanalyst.com/fifa-world-cup-2022/')
        time.sleep(random.randint(10, 20))

        players_button = driver.find_element("xpath", '//*[@id="Player Stats"]')
        teams_button = driver.find_element("xpath", '//*[@id="Team Stats"]')
        buttons = {"players": players_button, "teams": teams_button}

        for button in buttons:
            driver.execute_script("arguments[0].click();", buttons[button])
            time.sleep(random.randint(10, 20))

            data = []
            pages = list(range(1, 27))

            headers = []
            if button == "players":
                for th in driver.find_elements("xpath", "//thead/tr[2]/th"):
                    headers.append(th.text)
            elif button == "teams":
                for th in driver.find_elements("xpath", "//thead/tr/th"):
                    headers.append(th.text)

            data.append(headers)

            if button == "players":
                for page in pages[:2]:
                    page_number = driver.find_element("xpath", '//*[@id="root"]/div/div/div/div[5]/div[2]/div[2]/div[3]/span').text
                    page_number = int(page_number.split(' ')[0])
                    if page == page_number:

                        rows = driver.find_elements("xpath", '//tbody/tr')
                        rows_len = len(rows)
                        print(rows_len)

                        columns = driver.find_elements("xpath", "//thead/tr[2]/th")
                        columns_len = len(columns)
                        print(columns_len)

                        for row in range(1, rows_len + 1):
                            each_row = []
                            for col in range(1, columns_len + 1):
                                element = driver.find_element("xpath", "//tr["+str(row)+"]/td["+str(col)+"]").text
                                each_row.append(element)
                            data.append(each_row)
                        # print(data)

                        if page_number < 26:
                            sleep_time = random.randint(10, 20)
                            next_page = driver.find_element("xpath",
                                                            '//*[@id="root"]/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
                            driver.execute_script("arguments[0].click();", next_page)
                            time.sleep(sleep_time)
                        else:
                            print("Data has been scraped")
            elif button == "teams":
                rows = driver.find_elements("xpath", '//tbody/tr')
                rows_len = len(rows)
                print(rows_len)

                columns = driver.find_elements("xpath", "//thead/tr/th")
                columns_len = len(columns)
                print(columns_len)

                for row in range(1, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//tr[" + str(
                            row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)

            pd = pandas.DataFrame(data)
            if button == "players":
                pd.to_csv("theanalyst_players.csv", index=False, header=False)
            elif button == "teams":
                pd.to_csv("theanalyst_teams.csv", index=False, header=False)
            yield {'row': data}

        driver.quit()
