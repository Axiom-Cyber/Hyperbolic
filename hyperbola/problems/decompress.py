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
        logs = []
        if guess(filepath) != None:
            compressed = False
            extension = guess(filepath).extension
            outpath = re.sub(r"\.[^.]*$", "", filepath)
            if extension == "zip":
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    compressed = True
                    zip_ref.extractall(outpath)
                    logs.append({"type": "text", "msg": "Decompressed zip"})
            elif extension == "gz":
                with gzip.open(filepath, 'rb') as f:
                    compressed = True
                    out = open(outpath, "x")
                    out.close()
                    out = open(outpath, "wb")
                    out.write(f.read())
                    out.close()
                    logs.append({"type": "text", "msg": "Decompressed gzip"})
            elif extension == "7z":
                with py7zr.SevenZipFile(filepath, 'r') as archive:
                    compressed = True
                    archive.extractall(path=outpath)
                    logs.append({"type": "text", "msg": "Decompressed 7zip"})
            elif extension == "tar":
                with tarfile.open(filepath, "r") as tar:
                    compressed = True
                    tar.extractall(outpath)
                    logs.append({"type": "text", "msg": "Untarred"})
            else:
                return {"logs": [], "newdata": [{"type": "filepath", "data": filepath}]}
            if os.path.isdir(outpath):
                for (dirpath, dirnames, filenames) in os.walk(outpath):
                    for file in filenames:
                        logs += self.return_solution(outpath + "/" + file, False)["logs"]
                    break
            else:
                logs += self.return_solution(outpath, False)["logs"]
            if compressed and not first:
                os.remove(filepath)
            return {"logs": logs, "newdata": [{"type": "filepath", "data": outpath}]}
        else:
            return {"logs": logs, "newdata": [{"type": "filepath", "data": filepath}]}