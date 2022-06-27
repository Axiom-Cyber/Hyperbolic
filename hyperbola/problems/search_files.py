import hyperbola
import os

@hyperbola.Commander.add_worker('typedfile', "filepath")
class Extension:
    def return_solution(self, path):
        if os.path.isdir(path):
            output = ""
            for (dirpath, dirnames, filenames) in os.walk(path):
                    for filename in filenames:
                        with open(filename, "r") as file:
                            try:
                                for line in file:
                                    try:
                                        for character in line:
                                            try:
                                                output += character
                                            except:
                                                pass
                                    except:
                                        pass
                            except:
                                pass
                    break
            return {'logs':[],'newdata':[{"type": "text", "data":output}]}
        else:
            output = ""
            try:
                with open(path, "r") as file:
                    try:
                        for line in file:
                            try:
                                for character in line:
                                    try:
                                        output += character
                                    except:
                                        pass
                            except:
                                pass
                    except:
                        pass
            except:
                pass
            return {'logs':[],'newdata':[{"type": "text", "data":output}]}
