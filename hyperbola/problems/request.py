import hyperbola
import re
import requests

@hyperbola.Commander.add_worker('text')
class Url:
    def return_solution(self, data):
        urls = re.findall(r'(?:[^\s\/\.]+\.[^\s\/\.]+)(?:\/\S*)*', data)
        return {'logs':[{'type':'text', 'msg':'url: ' + i} for i in urls],'newdata':[{'type':'url','data':i.strip('/')} for i in urls]}

@hyperbola.Commander.add_worker('url')
class Webpage:
    def return_solution(self, data):
        rets = []
        logs = []
        for i in [requests.get, requests.post, requests.delete, requests.head, requests.patch, requests.put]:
            try:
                req = i('http://' + data)
                logs.append({'type':'text','msg':'responce found for ' + data})
                rets.append(req)
            except: pass
        return {'logs':logs,'newdata':[{'type':'request', 'data':i} for i in rets]}

@hyperbola.Commander.add_worker('request')
class Cookies:
    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':'text', 'data':i} for i in data]}

@hyperbola.Commander.add_worker('url')
class Robots:
    def return_solution(self, data):
        base = re.search(r'(https?:\/\/)?(.+?)(?=\/|\s|$)', data).groups(2)
        return {'logs':[], 'newdata':[{'type':'request','data':i+'/robots.txt'} for i in [base, data]]}

@hyperbola.Commander.add_worker('request')
class Relatives:
    def return_solution(self, data):
        base = re.search(r'(https?:\/\/)?(.+?)(?=\/|\s|$)', data.url).groups(2)
        return {'logs':[], 'newdata':[{'type':'url', 'data':base+i} for i in re.findall(r'/\S+', data.text)]}

@hyperbola.Commander.add_worker('request')
class Page:
    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type': 'text', 'data': data.text}]+
          [{'type':'text', 'data':data.text.replace(r'<.*?>', '')}]}

@hyperbola.Commander.add_worker('request')
class Headers:
    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':'text', 'data':', '.join([i+': '+j for i,j in data.raw.headers.items() if type(i)==type(j)==str])}]}