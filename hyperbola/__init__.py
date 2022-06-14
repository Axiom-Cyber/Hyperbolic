from os.path import dirname, basename, isfile, join
import glob

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

    @classmethod
    def run(self, type, data, maxDepth=100, logger = None):
        c = self(maxDepth, logger)
        
        for i in c.detectors[type]:
            asyncio.create_task(c.run_node(i, data))

    def __init__(self, maxDepth, logger):
        self.running = True
        self.logger = logger
        self.maxDepth = maxDepth
            

    async def run_node(self, problem, data, layers = 0):
        if not self.running or layers > self.maxDepth:
            return
        exec = problem()
        ret = await exec.return_solution(data)
        if self.logger!=None and 'logs' in ret:
            for i in ret['logs']:
                await self.logger(i)
        if ret['end']:
            self.running = False
            return
        if ret and 'newdata' in ret:
            for i in ret['newdata']:
                for j in self.detectors[i['type']]:
                    asyncio.create_task(self.run_node(i['type'], i['data'], layers + 1))

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
        flag = re.match(self.flag, data)
        if flag:
            return {'logs' : ['flag found: ' + flag.group()], 'end':True}

prob = glob.glob(join(dirname(__file__), 'problems', "*.py"))
__all__ =  [basename(f)[:-3] for f in prob if isfile(f)]