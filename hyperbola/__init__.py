from os.path import dirname, basename, isfile, join

import re
import math
import os

class Commander:
    final_name='Flag'
    final_type='text'

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

    def __init__(self, final_re, logger, saf_dir, max_depth):
        self.final_re = final_re
        self.logger = logger
        self.max_depth = max_depth
        self.safe_functions = {i:__builtins__[i] for i in __builtins__}
        self.safe_functions['re'] = re
        self.safe_functions['math'] = math
        self.safe_functions['join'] = os.path.join
        del self.safe_functions['quit']
        del self.safe_functions['print']
        self.safe_functions['open'] = lambda a,b='rt',encoding='ascii': open(a,b,encoding=encoding) if re.search(r'^(\.\/)?'+self.safe_dir, os.path.normpath(a)) else None

    @classmethod
    def run(cls, section, data, logger, safe_dir='', user_data={}, disabled_solvers=[], flag=r'flag\{\S*?\}', max_depth=5):
        self = cls(flag, logger, safe_dir, max_depth)
        children = [{'type':section, 'data':data}]
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
                    nchildren += ret['newdata']
                if i['type'] in user_data:
                    for j in range(len(user_data[i['type']])):
                        print(j)
                        try:
                            ret = None
                            l = {m:n for m,n in self.safe_functions.items()}
                            exec('def return_solution(data): \n  '+user_data[i['type']][j].replace('\n', '\n  '), {'__builtins__':None}, l)
                            ret = l['return_solution'](i['data'])
                            for log in ret['logs']:
                                self.logger(log['type'], log['msg'])
                            nchildren += ret['newdata']
                        except Exception as ex:
                            msg = "An exception in activated user code #{0} of type {1} occurred. Arguments:\n{2!r}".format(j+1, type(ex).__name__, ex.args)
                            self.logger('text', msg)
                if i['type'] == self.final_type and self.final_name not in disabled_solvers:
                    flag = self.check_flag(i['data'])
                    if flag != False:
                        self.logger('text', self.final_name + ' found: ' + flag)
                        self.logger('end', 'task exited')
                        return
            children = nchildren
        self.logger('end', 'task exited')
    @classmethod
    def compile_names(self):
        names = [self.final_name]
        for i in self.detectors:
            for j in self.detectors[i]:
                if j.__name__ not in names:
                    names.append(j.__name__)
        return names

    def check_flag(self, str):
        flag = re.search(self.final_re, str)
        if flag!=None:
            return flag.group()
        return False

class Problem:
    def return_solution(self, data):
        return {'logs':[], 'newdata':[{'type':None,'data':None}]}

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