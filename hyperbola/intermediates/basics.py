import defaults
import re
import requests

@defaults.Commander.add_worker('text')
class Website(defaults.Problem):
    async def spotlight(self, data):
        return True
    
    async def return_solution(self, data):
        return {'logs':[],'newdata':['url':i for i in re.findall(r'((?:https?:\/\/)?[^\s/]*?\.[^\s/]*?)\/\S*', data)]}

@defaults.Commander.add_worker('url')
class Request:
    async def spotlight(self, data):
        return True
    
    async def return_solution(self, data):
        post = requests.post(data).text
        get = requests.get(data).text
        rets = []
        logs = []
        if post: 
            logs.append('responce found for post on ' + data)
            rets.append(post.text)
        if get: 
            logs.append('responce found for get on ' + data)
            rets.append(get.text)
        return {'logs':logs,'newdata':['text':i for i in rets]}