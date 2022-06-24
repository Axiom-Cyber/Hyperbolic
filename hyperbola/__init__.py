from os.path import dirname, basename, isfile, join
import glob

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

    def __init__(self, logger, max_depth):
        self.logger = logger
        self.max_depth = max_depth

    @classmethod
    def run(cls, type, data, logger, max_depth=5):
        self = cls(logger, max_depth)
        children = [[data, i] for i in self.detectors[type]]
        for _ in range(max_depth):
            nchildren = []
            for i in children:
                data = self.run_node(i, data)
                if data[0]:
                    _ = False 
                    break
                nchildren += data[1]
            if _ == False: break
            children = nchildren
        self.logger('end', 'task exited')

    def run_node(self, problem, data, layers = 0):
        exec = problem()
        ret = exec.return_solution(data)

        for i in ret['logs']:
            self.logger(i['type'], i['msg'])
        children = []
        for i in ret['newdata']:
            for j in self.detectors[i['type']]:
                children.append([j, i['data']])
        
        return ret['end'], children

class Problem:
    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}

@Commander.add_worker('text')
class Flag(Problem):
    flag = r'flag\{\S*?\}'
    @classmethod
    def set_flag(self, flag):
        self.flag = flag
    def return_solution(self, data):
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