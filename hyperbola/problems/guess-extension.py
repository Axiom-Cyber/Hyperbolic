from filetype import guess
import hyperbola

@hyperbola.Commander.add_worker('filepath')
class Extension:
    async def return_solution(self, filepath):
        guess = guess(filepath)
        if guess:
            return {'logs':[],'newdata':[{"type": "extension", "data":guess.extension}],'end':False}
        else:
            return {'logs':[],'newdata':[{"type": "extension", "data":None}],'end':False}