import hyperbola
import os

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, path):
        if os.isdir(path):
            output = ""
            for (dirpath, dirnames, filenames) in os.walk(path):
                    for filename in filenames:
                        with open(filename, "r") as file:
                            output += file.read()
                    break
            return {'logs':[],'newdata':[{"type": "text", "data":output}],'end':False}