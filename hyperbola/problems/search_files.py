import hyperbola
import os

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, path):
        if os.path.isdir(path):
            output = ""
            for (dirpath, dirnames, filenames) in os.walk(path):
                    for filename in filenames:
                        with open(filename, "r") as file:
                            for line in file:
                                try:
                                    for character in line:
                                        try:
                                            output += character
                                        except:
                                            pass
                                except:
                                    pass
                    break
            return {'logs':[],'newdata':[{"type": "text", "data":output}],'end':False}
        else:
            with open(path, "rb") as file:
                output = ""
                for line in file:
                    try:
                        for character in line:
                            try:
                                output += character
                            except:
                                pass
                    except:
                        pass
            return {'logs':[],'newdata':[{"type": "text", "data":output}],'end':False}