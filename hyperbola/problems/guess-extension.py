from filetype import guess
import hyperbola
from os import rename
import re

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, filepath):
        guess = guess(filepath)
        if guess:
            rename(filepath, re.sub(r"\.[^.]*$", "", filepath) + "." + guess.extension)
            return {'logs':[guess.extension],'newdata':[{"type": "extension", "data":guess.extension}],'end':False}
        else:
            return {'logs':[],'newdata':[{"type": "extension", "data":None}],'end':False}