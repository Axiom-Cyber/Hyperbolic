from os.path import dirname, basename, isfile, join

import re
import math
import os

class Commander:
    safe_functions = {i:__builtins__[i] for i in __builtins__}
    safe_functions['re'] = re
    safe_functions['math'] = math
    safe_functions['open'] = lambda a,b='rt',encoding=ascii: open(a,b,encoding=encoding) if re.search(r'^(\.\/)?flaskapp/UploadedFiles', os.path.normpath(a)) else None
    safe_functions['join'] = os.path.join
    del safe_functions['quit']
    del safe_functions['print']

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
    def run(cls, type, data, logger, user_data={}, disabled_solvers=[], max_depth=5):
        self = cls(logger, max_depth)
        children = [{'type':type, 'data':data}]
        for _ in range(max_depth):
            nchildren = []
            for i in children:
                for j in self.detectors[i['type']]:
                    if j.__name__ in disabled_solvers:
                        continue
                    e = j()
                    ret = e.return_solution(i['data'])
                    for log in ret['logs']:
                        self.logger(log['type'], log['msg'])
                    if ret['end']:
                        _ = False 
                        break
                    nchildren += ret['newdata']
                if i['type'] in user_data:
                    for j in user_data[i['type']]:
                        try:
                            print('def return_solution(data): \n  '+j.replace('\n', '\n  '))
                            ret = None
                            l = {m:n for m,n in self.safe_functions.items()}
                            exec('def return_solution(data): \n  '+j.replace('\n', '\n  '), {'__builtins__':None}, l)
                            print(l['return_solution'])
                            ret = l['return_solution'](i['data'])
                            for log in ret['logs']:
                                self.logger(log['type'], log['msg'])
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

def add_solver(bin, name, desc):
    try:
        path = os.path.join('hyperbola','problems', name)
        desc = re.sub(re.compile(r'^', re.M),'# ', desc)
        with open(path, 'xb') as f:
            f.write(bin)
        with open(path, 'at') as f:
            f.write(desc)
        __import__(prefix + path.replace(r'^(.*?)(\.py?)$','\1').replace(r'(\\*?|\/*?)', '.'), locals(), globals())
    except: return False
    return True