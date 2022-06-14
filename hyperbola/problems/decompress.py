from filetype import guess
import zipfile
from os import walk

#@defaults.Commander.add_worker('filepath')
#class Decompress:
def decompress(filepath, out):
    if guess(filepath) != None and guess(filepath).extension == "zip":
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(out)
            for (dirpath, dirnames, filenames) in walk(out):
                for file in filenames:
                    decompress(out + "/" + file, out + "/" + file[::-4])
                break

decompress(input(), "C:/Users/clemevin000/Desktop/out")