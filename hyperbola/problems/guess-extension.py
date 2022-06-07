from filetype import guess
import defaults

def guessExtension(filePath):
    try:
        print("Filetype: " + str(guess(filePath).extension))
    except:
        print("Couldn't find filetype")

if __name__ == "__main__":
    guessExtension()