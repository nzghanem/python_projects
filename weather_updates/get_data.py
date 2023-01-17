from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WeatherData():
    def __init__(self, url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def __iter__(self):
        return iter(self.weather())

    def get_data(self):
        data = self.driver.find_element(
            By.CLASS_NAME, "cardContainer-E1_2").text
        slider = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/div/div[2]/button")))
        slider.click()
        time.sleep(10)
        return data.split("\n")

    def weather(self):
        all_data = []
        try:
            pop = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "onetrust-accept-btn-handler")))
            pop.click()
        except:
            pass
        all_data.append([self.get_data(),
                        self.get_data()])
        realFeel = self.driver.find_element(
            By.ID, "OverviewCurrentTemperature").text
        all_data.append("FEELS" + realFeel.split("FEELS")[1])
        temp = []
        for i in range(10):
            try:
                button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/ul/li[{i+1}]/button/span/div/div/div[2]/div[1]/div")))
                button.click()
                condition = self.driver.find_element(
                    By.CLASS_NAME, "cap-E1_1").text
                temp.append(condition)
            except:
                print("Failed Operation")

        all_data.append(temp)
        self.driver.quit()
        return all_data


# print(list(WeatherData("https://www.msn.com/en-us/weather/forecast/in-Brno,South-Moravia?ocid=ansmsnweather&loc=eyJsIjoiQnJubyIsInIiOiJTb3V0aCBNb3JhdmlhIiwicjIiOiJCcm5vIC0gbcSbc3RvIiwiYyI6IkN6ZWNoaWEiLCJpIjoiQ1oiLCJnIjoiZW4tdXMiLCJ4IjoiMTYuNDkiLCJ5IjoiNDkuMjEifQ%3D%3D&weadegreetype=C"))[2])
