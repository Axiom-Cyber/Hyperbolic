'''
flag 'flag\{\w{4,50}\}'
binary [01]{8,}
hex [0-9A-Fa-f]{2,}
url http\w+
'''

from contextlib import AsyncExitStack
import subprocess
import re
#import magic

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# result = subprocess.run(['python3', '--version'], capture_output=True, encoding='UTF-8')
# patoolib.extract_archive("archive.zip", outdir="temp")

'''

'''
class Inspector:
    def __init__(self, worker: object, title, points, description, category, tags, attached_files):
        self.worker = worker
        self.title = title
        self.points = points
        self.description = description
        self.category = category
        self.tags = tags
        self.attached_files = attached_files

    def sort_file(self):
        self.filetype = magic.from_file(self.path)
    
    def extract_decompress_file(self):
        pass

class Worker:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        self.login()

    def login(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path='C:\\Users\\nacanjak000\\Documents\\chromedriver.exe', options=options)

        driver.get(f'{self.url}/login')

        driver.find_element(By.ID, 'name').send_keys(self.username)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, '_submit').submit()

        print(driver.page_source)
        
        driver.close()

    def get_problems(self):
        pass

    def get_scores(self):
        pass

    def get_stats(self):
        pass

    def submit_flag(self):
        pass

if __name__ == '__main__':
    w = Worker('https://demo.ctfd.io/', 'user', 'password')