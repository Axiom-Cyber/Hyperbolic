import filetype
import hyperbola
import re

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, filepath):
        guess = filetype.guess(filepath)
        if guess:
            outpath = re.sub(r"\.[^.]*$", "", filepath) + "." + guess.extension
            with open(filepath, "rb") as filein:
                with open(outpath, "wb") as fileout:
                    fileout.write(filein.read())
            return {'logs':[{"type": "text", "msg": guess.extension}],'newdata':[{"type": "typedfile", "data":outpath}],'end':False}
        else:
            return {'logs':[],'newdata':[{"type": "typedfile", "data":filepath}],'end':False}