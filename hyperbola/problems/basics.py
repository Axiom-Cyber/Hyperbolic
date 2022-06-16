import hyperbola
import re
import requests

@hyperbola.Commander.add_worker('text')
class Website:
    async def return_solution(self, data):
        urls = re.findall(r'(?:[^\s\/\.]+\.[^\s\/\.]+)(?:\/\S*)*', data)
        return {'logs':['url: ' + i for i in urls],'newdata':[{'type':'url','data':i} for i in urls], 'end':False}

@hyperbola.Commander.add_worker('url')
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
        return {'logs':logs,'newdata':[{'type':'text', 'data':i} for i in rets] + 
          [{'type':'text', 'data':i.replace(r'<.*?>', '')} for i in rets],
          'end':False}