from os.path import dirname, basename, isfile, join
import glob

import asyncio
import re
import os

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

    @classmethod
    def run(self, type, data, logger, maxDepth=5):
        c = self(maxDepth, logger)
        async def start():
            for i in self.detectors[type]:
                if c.running and maxDepth:
                    c.running_nodes+=1
                    asyncio.create_task(c.run_node(i, data))
        asyncio.run(start())
    def __init__(self, maxDepth, logger):
        self.running = True
        self.logger = logger
        self.maxDepth = maxDepth
        self.running_nodes = 0

    async def run_node(self, problem, data, layers = 0):
        exec = problem()
        ret = await exec.return_solution(data)

        for i in ret['logs']:
            await self.logger(i['type'], i['msg'])
        if not ret['end']:
            for i in ret['newdata']:
                for j in self.detectors[i['type']]:
                    if self.running and layers < self.maxDepth-1:
                        self.running_nodes+=1
                        await self.run_node(j, i['data'], layers+1)
        else:
            self.running = False
                
        self.running_nodes-=1
        if self.running_nodes<=0:
            await self.logger('end', 'task exited')

class Problem:
    async def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}

@Commander.add_worker('text')
class Flag(Problem):
    flag = r'flag\{\S*?\}'
    @classmethod
    def set_flag(self, flag):
        self.flag = flag
    async def return_solution(self, data):
        flag = re.search(self.flag, data)
        if flag!=None:
            return {'logs' : [{'type':'text', 'msg':'flag found: ' + flag.group()}], 'newdata':[], 'end':True}
        return {'logs' : [], 'newdata' : [], 'end':False}

prefix = 'problems.'
if __name__ != '__main__':
    prefix = __name__ + '.' + prefix
for module in os.listdir(os.path.join(os.path.dirname(__file__), 'problems')):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(prefix + module[:-3].replace(r'(\\*?|\/*?)', '.'), locals(), globals())
del module