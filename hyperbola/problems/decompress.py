from filetype import guess
import zipfile
from os import walk

@defaults.Commander.add_worker('filepath')
class Decompress:
    def decompress(self, filepath):
        if guess(filepath) != None and guess(filepath).extension == "zip":
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(filepath[:-4])
                for (dirpath, dirnames, filenames) in walk(filepath[:-4]):
                    for file in filenames:
                        self.decompress(filepath[:-4] + "/" + file)
                    break