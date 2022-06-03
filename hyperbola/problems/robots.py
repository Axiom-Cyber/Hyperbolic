import defaults
import requests
import re
defaults.Commander.add_worker('url')
class Robots:
    async def return_solution(self, data):
        nurl = data.replace(r'((?:https?:\/\/)?.*?)\/.*', '\1')
        newdata = []
        try:
            req = requests.get(nurl)
            newdata.append(req.text)
        except: pass
        try:
            req = requests.post(nurl)
            newdata.append(req.text)
        except: pass
        for i in newdata:
            pass
        return {'logs':[], 'newdata'[{'type':'text','data':i} for i in newdata]}