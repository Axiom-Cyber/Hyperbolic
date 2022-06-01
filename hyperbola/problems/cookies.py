import defaults
import requests
defaults.Commander.add_worker('url')
class Cookie:
    async def return_solution(self, data):
        post = requests.post(data)
        try:
            get = requests.get(data)