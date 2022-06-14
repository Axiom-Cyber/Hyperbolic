import defaults
import requests
@defaults.Commander.add_worker('url')
class Cookie:
    async def return_solution(self, data):
        post = requests.post(data)
        newdata = []
        try:
            get = requests.get(data)
            for c in get.cookies:
                newdata.append(c.name)
                newdata.append(c.name)
        except: pass
        try:
            post = requests.post(data)
            for c in post.cookies:
                newdata.append(c.name)
                newdata.append(c.name)
        except: pass
        return {'logs':[], 'newdata':[{'type':'text', 'data':i} for i in newdata]}