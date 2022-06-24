from os.path import dirname, basename, isfile, join

import re
import math
import os

class Commander:
    safe_functions = __builtins__ + {'re':re, 'math':math}
    safe_functions['open'] = lambda a,b='rt': open(a,b) if re.search(r'^(\.\/)?flaskapp/UploadedFiles', os.path.normpath(a)) else None
    safe_functions['join'] = os.path.join
    del safe_functions['quit']

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
    def run(cls, type, data, logger, user_data={}, max_depth=5):
        self = cls(logger, max_depth)
        children = [{'type':type, 'data':data}]
        for _ in range(max_depth):
            nchildren = []
            for i in children:
                for j in self.detectors[i['type']]:
                    e = j()
                    ret = e.return_solution(i['data'])
                    for i in ret['logs']:
                        self.logger(i['type'], i['msg'])
                    if ret['end']:
                        _ = False 
                        break
                    nchildren += ret['newdata']
                print(user_data, i['type'])
                if i['type'] in user_data:
                    for j in user_data[i['type']]:
                        try:
                            exec('def return_solution(data): \n  '+j.replace('\n', '\n  '), self.safe_functions, None)
                            ret = return_solution(i['data'])
                            for i in ret['logs']:
                                self.logger(i['type'], i['msg'])
                            if ret['end']:
                                _ = False 
                                break
                            nchildren += ret['newdata']
                        except: pass
            if _ == False: break
            children = nchildren
        self.logger('end', 'task exited')

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