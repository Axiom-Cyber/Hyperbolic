import defaults
import re
import requests

@defaults.Commander.add_worker('text')
class Website(defaults.Problem):
    async def return_solution(self, data):
        return {'logs':[],'newdata':[{'type':'url','data':i} for i in re.findall(r'((?:https?:\/\/)?[^\s/]*?\.[^\s/]*?)\/\S*', data)]}

@defaults.Commander.add_worker('url')
class Request:
    async def return_solution(self, data):
        rets = []
        logs = []
        try:
            post = requests.post(data)
            logs.append('responce found for post on ' + data)
            rets.append(post.text)
        except: pass
        try:
            get = requests.get(data)
            logs.append('responce found for get on ' + data)
            rets.append(get.text)
        except: pass
        return {'logs':logs,'newdata':[{'type':'text', 'data':i} for i in rets], 'end':False}