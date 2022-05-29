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

    def run_tree(self, type, data):
        for i in self.detectors[type]:
            spotlight = i.spotlight(data)
            if spotlight:
                asyncio.create_task(self.run_node(i, data))
            

    async def run_node(self, problem, data):
        if self.found_flag:
            return
        exec = problem()
        ret = exec.return_solution(data)
        if self.logger and 'logs' in ret:
            for i in ret['logs']:
                self.logger(i)
        if 'flag' in ret:
            self.found_flag = True
            return
        if ret and 'newdata' in ret:
            for i in ret['newdata']:
                for j in self.detectors[i['type']]:
                    spotlight = j.spotlight(i['data'])
                    if spotlight:
                        asyncio.create_task(self.run_node(i, i['data']))
   
class Logger:
    def __call__(txt):
        pass

class Problem:
    def spotlight(self, data):
        return True

    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}

@Commander.add_worker('text')
class Flag(Problem):
    @classmethod
    def set_flag(self, flag):
        self.flag = flag

    def spotlight(self, data):
        return True
    def return_solution(self, data):
        flag = re.find(r'((?:https?:\/\/)?[^\s/]*?\.[^\s/]*?)\/\S*', data)
        if flag:
            return {'logs' : ['flag found: ' + flag], 'flag':1}