import hyperbola
import requests
import re
@hyperbola.Commander.add_worker('url')
class Robots:
    async def return_solution(self, data):
        nurl = 'http://' + data.replace(r'([^/].*?)\/.*', '\1')
        newdata = []
        links = []
        for i in [nurl, data]:
            for j in [requests.get, requests.post]:
                try:
                    req = j(i + '/robots.txt')
                    for k in re.findAll(r'[Aa]llow[ \t]*?:[ \t]*?(\S+)', req.text):
                        links.append(nurl + k.groups(1))
                    newdata.append(req)
                except: pass
        return {'logs':[], 'newdata':[{'type':'request','data':i} for i in newdata] + [{'type':'url','data':i} for i in links], 'end':False}