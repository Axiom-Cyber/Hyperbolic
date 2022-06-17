import hyperbola
import re
import requests

@hyperbola.Commander.add_worker('text')
class Url:
    async def return_solution(self, data):
        urls = re.findall(r'(?:[^\s\/\.]+\.[^\s\/\.]+)(?:\/\S*)*', data)
        return {'logs':['url: ' + i for i in urls],'newdata':[{'type':'url','data':i.strip('/')} for i in urls], 'end':False}

@hyperbola.Commander.add_worker('url')
class Request:
    async def return_solution(self, data):
        rets = []
        logs = []
        for i in [requests.get, requests.post]:
            try:
                req = i(data)
                logs.append('responce found for ' + data)
                rets.append(req)
            except: pass
        return {'logs':logs,'newdata':[{'type':'request', 'data':i} for i in rets],
          'end':False}
@hyperbola.Commander.add_worker('request')
class Cookie:
    async def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':'text', 'data':i} for i in data], 'end':False}
@hyperbola.Commander.add_worker('request')
class Page:
    async def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type': 'text', 'data': data.text}]+
          [{'type':'text', 'data':data.text.replace(r'<.*?>', '')}], 'end':False}