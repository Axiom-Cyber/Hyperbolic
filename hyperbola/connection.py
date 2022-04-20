from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Worker:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        self.login()

        print('Worker logged in')

        self.load_problems()

        print('Worker problems loaded')
    
    def __str__(self) -> str:
        out = ''
        for category in self.problems:
            out += '\n' + '=' * (len(category) + 8) + '\n'
            out += f'=== {category.upper()} ===\n'
            out += '=' * (len(category) + 8) + '\n\n'

            for problem in self.problems[category]:
                out += '---\n'
                out += f"Name: {problem['name']}\n"
                out += f"Points: {problem['points']}\n"
                out += f"Description: {problem['description']}\n"
                out += '---\n'

        return out
    
    def __repr__(self) -> str:
        return str(self.problems)

    def login(self):
        options = FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

        self.wait = WebDriverWait(self.driver, 100)

        self.driver.get(f'{self.url}/login')

        self.driver.find_element(By.ID, 'name').send_keys(self.username)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.ID, '_submit').submit()

        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'challenge-button')))
        except Exception:
            print('Login fail')
    
    def close(self):
        self.driver.close()

    def load_problems(self):
        problems = {}
        html_category_rows = self.driver.find_elements(By.CSS_SELECTOR, 'div#challenges-board > div')

        for c in html_category_rows:
            category_title = c.find_element(By.TAG_NAME, 'h3').text
            problems[category_title] = []
            html_listed_problems = c.find_elements(By.CLASS_NAME, 'challenge-button')
            for p in html_listed_problems:
                sleep(1) # I have tried for a while to use wait instead but can't find a solution
                p.click()
                problem = {}
                problem['name'] = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'challenge-name'))).text
                problem['points'] = self.driver.find_element(By.CLASS_NAME, 'challenge-value').text
                problem['description'] = self.driver.find_element(By.CLASS_NAME, 'challenge-desc').text

                # Still need to add file downloading

                problems[category_title].append(problem)
                self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'close'))).click()
                sleep(1)
        
        self.problems = problems

    def get_scores(self):
        pass

    def get_stats(self):
        pass

    def submit_flag(self):
        pass