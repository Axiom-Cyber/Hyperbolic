from filetype import guess
import zipfile
import os
import hyperbola
import gzip
import re
import py7zr

@hyperbola.Commander.add_worker('filepath')
class Decompress:
    def decompress(self, filepath):
        if guess(filepath) != None:
            compressed = False
            extension = guess(filepath).extension
            outpath = re.sub(r"\.[^.]*$", "", filepath)
            if extension == "zip":
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    compressed = True
                    zip_ref.extractall(outpath)
            elif extension == "gz":
                with gzip.open(filepath, 'rb') as f:
                    compressed = True
                    out = open(outpath, "x")
                    out.close()
                    out = open(outpath, "w")
                    out.write(f.read())
                    out.close()
            elif extension == "7z":
                with py7zr.SevenZipFile(filepath, 'r') as archive:
                    compressed = True
                    archive.extractall(path=outpath)
            if os.path.isdir(outpath):
                for (dirpath, dirnames, filenames) in os.walk(outpath):
                    for file in filenames:
                        self.decompress(outpath + "/" + file)
                    break
            elif compressed:
                self.decompress(outpath)
            else:
                return(outpath)