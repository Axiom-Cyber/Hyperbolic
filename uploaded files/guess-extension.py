import filetype

def guessExtension(filePath):
    try:
        print("Filetype: " + str(filetype.guess(filePath).extension))
    except:
        print("Couldn't find filetype")

if __name__ == "__main__":
    guessExtension()