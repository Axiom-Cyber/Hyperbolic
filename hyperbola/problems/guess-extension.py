from filetype import guess
import hyperbola

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def return_solution(self, filePath):
        try:
            print("Filetype: " + str(guess(filePath).extension))
        except:
            print("Couldn't find filetype")
        return {'logs':[],'newdata':[],'end':False}