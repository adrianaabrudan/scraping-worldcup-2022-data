import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
import time
import random
import pandas


class TheAnalystSpider(scrapy.Spider):
    name = 'mykhel'
    # allowed_domains = ['www.dataviz.theanalyst.com']
    # start_urls = ['https://dataviz.theanalyst.com/fifa-world-cup-2022/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.mykhel.com/football/fifa-world-cup-2022-player-stats-l4/',
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=r'./chromedriver')
        driver.get('https://www.mykhel.com/football/fifa-world-cup-2022-player-stats-l4/')
        time.sleep(random.randint(10, 20))

        overview = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[1]/a')
        goals = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[2]/a')
        goal_type = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[3]/a')
        attempts = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[4]/a')
        passes = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[5]/a')
        defence = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[6]/a')
        disciplinary = driver.find_element("xpath", '//*[@id="db_js_team_ranking"]/div[2]/div[1]/div[2]/div/div[1]/ul/li[7]/a')
        buttons = {"overview": overview, "goals": goals, "goal_type": goal_type,
                   "attempts": attempts, "passes": passes, "defence": defence, "disciplinary": disciplinary}

        for index, button in enumerate(buttons):
            driver.execute_script("arguments[0].click();", buttons[button])
            time.sleep(random.randint(10, 20))
            data = []
            headers = []
            if button == "overview":
                for th in driver.find_elements("xpath", '//*[@id="overview_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="overview_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='overview_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='overview_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_overview.csv", index=False,header=False)

            elif button == "goals":
                for th in driver.find_elements("xpath", '//*[@id="goals_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="goals_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='goals_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='goals_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_goals.csv", index=False, header=False)

            elif button == "goal_type":
                for th in driver.find_elements("xpath", '//*[@id="types_of_goals_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="types_of_goals_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='types_of_goals_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='types_of_goals_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_types_of_goals.csv", index=False, header=False)

            elif button == "attempts":
                for th in driver.find_elements("xpath", '//*[@id="attempts_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="attempts_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='attempts_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='attempts_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_attempts.csv", index=False, header=False)

            elif button == "passes":
                for th in driver.find_elements("xpath", '//*[@id="passes_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="passes_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='passes_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath","//*[@id='passes_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_passes.csv", index=False, header=False)

            elif button == "defence":
                for th in driver.find_elements("xpath", '//*[@id="defence_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="defence_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='defence_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='defence_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_defence.csv", index=False, header=False)
            elif button == "disciplinary":
                for th in driver.find_elements("xpath", '//*[@id="disciplinary_loading_body"]/tr[1]/th'):
                    headers.append(th.text)
                data.append(headers)
                rows = driver.find_elements("xpath", '//*[@id="disciplinary_loading_body"]/tr')
                rows_len = len(rows)
                columns = driver.find_elements("xpath", "//*[@id='disciplinary_loading_body']/tr[1]/th")
                columns_len = len(columns)
                for row in range(2, rows_len + 1):
                    each_row = []
                    for col in range(1, columns_len + 1):
                        element = driver.find_element("xpath", "//*[@id='disciplinary_loading_body']/tr[" + str(row) + "]/td[" + str(col) + "]").text
                        each_row.append(element)
                    data.append(each_row)
                print(data)
                pd = pandas.DataFrame(data)
                pd.to_csv("mykhel_files/mykhel_disciplinary.csv", index=False, header=False)
            yield data
        driver.quit()
