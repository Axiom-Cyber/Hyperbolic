import asyncio

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
                asyncio.create_task(self.run_node(i, spotlight))
            

    async def run_node(self, problem, data):
        if self.found_flag:
            return
        exec = problem()
        ret = exec.return_solution(data)
        if self.logger:
            for i in ret['logs']:
                self.logger(i)
        for i in ret['newdata']:
            for j in self.detectors[i['type']]:
                spotlight = j.spotlight(i['data'])
                if spotlight:
                    asyncio.create_task(self.run_node(j, spotlight))
   
class Logger:
    def __call__(txt):
        pass

@Commander.add_worker('default')
class Problem:
    def __init__(self):
        self.outputs = []

    def spotlight(self, data):
        return None

    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}