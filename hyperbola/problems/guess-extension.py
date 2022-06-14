from filetype import guess
import hyperbola

@hyperbola.Commander.add_worker('filepath')
class Extension:
    def guessExtension(filePath):
        try:
            print("Filetype: " + str(guess(filePath).extension))
        except:
            print("Couldn't find filetype")