from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import hyperbola

@hyperbola.Commander.add_worker('url')
class Forms:
    def return_solution(self, data):
        driver = webdriver.Firefox()
        driver.get(data)
        forms = driver.find_elements(By.TAG_NAME, 'form')
        newdata = []
        for i in forms:
            i.submit()
            if driver.current_url != data:
                newdata.append(driver.current_url)
                driver.get(data)

        driver.close()

        return {'logs':[{'type':'text', 'msg':i} for i in newdata], 'newdata':[{'type':'text', 'newdata':i} for i in newdata]}