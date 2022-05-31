import asyncio
import re

class Commander:
    detectors = {}
    
    @classmethod
    def add_worker(self, *categories):
        def decorate(clss):
            for i in categories:
                if i in self.detectors:
                    self.detectors[i].append(clss)
                else: self.detectors[i] = [clss]
            return clss
        return decorate

    def __init__(self, logger = None):
        self.found_flag = False
        self.logger = logger
    
    def run(self, type, data):
        asyncio.run(c.run_tree(type, data))

    async def run_tree(self, type, data):
        for i in self.detectors[type]:
            spotlight = await i.spotlight(data)
            if spotlight:
                asyncio.create_task(self.run_node(i, data))
            

    async def run_node(self, problem, data):
        if self.found_flag:
            return
        exec = problem()
        ret = await exec.return_solution(data)
        if self.logger!=None and 'logs' in ret:
            for i in ret['logs']:
                await self.logger(i)
        if 'flag' in ret:
            self.found_flag = True
            return
        if ret and 'newdata' in ret:
            for i in ret['newdata']:
                for j in self.detectors[i['type']]:
                    spotlight = await j.spotlight(i['data'])
                    if spotlight:
                        asyncio.create_task(self.run_node(i['type'], i['data']))
   
class Logger:
    async def __call__(self, txt):
        print(txt)

class Problem:
    async def spotlight(self, data):
        return True

    async def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}

@Commander.add_worker('text')
class Flag(Problem):
    @classmethod
    def set_flag(self, flag):
        self.flag = flag
    @classmethod
    async def spotlight(self, data):
        return True
    async def return_solution(self, data):
        flag = re.match(r'flag\{\S*?\}', data)
        if flag:
            return {'logs' : ['flag found: ' + flag.group()], 'flag':1}

l = Logger()
c = Commander(l)
c.run('text', 'flag{1223ss}')