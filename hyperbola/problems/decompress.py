from filetype import guess
import zipfile
import os

from sqlalchemy import false
import hyperbola
import gzip
import re
import py7zr
import tarfile

@hyperbola.Commander.add_worker('filepath')
class Decompress:
    def return_solution(self, filepath, first=True):
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
                    out = open(outpath, "wb")
                    out.write(f.read())
                    out.close()
            elif extension == "7z":
                with py7zr.SevenZipFile(filepath, 'r') as archive:
                    compressed = True
                    archive.extractall(path=outpath)
            elif extension == "tar":
                with tarfile.open(filepath, "r") as tar:
                    compressed = True
                    tar.extractall(outpath)
            if os.path.isdir(outpath):
                for (dirpath, dirnames, filenames) in os.walk(outpath):
                    for file in filenames:
                        self.decompress(outpath + "/" + file, False)
                    break
            else:
                self.decompress(outpath, False)
            if compressed and not first:
                os.remove(filepath)
        return {"logs": [], "newdata": [{"type": "filepath", "data": outpath}], "end": False}