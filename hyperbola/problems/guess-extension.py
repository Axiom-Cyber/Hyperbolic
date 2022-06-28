import filetype
import hyperbola
import re
import os

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, filepath):
        if not os.path.isdir(filepath):
            guess = filetype.guess(filepath)
            if guess:
                outpath = re.sub(r"\.[^.]*$", "", filepath) + "." + guess.extension
                with open(filepath, "rb") as filein:
                    with open(outpath, "wb") as fileout:
                        fileout.write(filein.read())
                return {'logs':[{"type": "text", "msg": "This file is a " + guess.extension}],'newdata':[{"type": "typedfile", "data":outpath}]}
            else:
                return {'logs':[{"type": "text", "msg": "Couldn't guess extension"}],'newdata':[{"type": "typedfile", "data":filepath}]}
        else:
            return{"logs":[], "newdata":[]}