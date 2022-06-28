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
    def return_solution(self, filepath, first=True, outpath = None):
        logs = []
        if not os.path.isdir(filepath) and guess(filepath) != None:
            compressed = False
            extension = guess(filepath).extension
            if first:
                outpath = re.sub(r"\.[^.]*$", "", filepath)
                os.mkdir(outpath)
                print("making " + outpath)
            if extension == "zip":
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    compressed = True
                    zip_ref.extractall(outpath)
                    logs.append({"type": "text", "msg": "Decompressed zip"})
            elif extension == "gz":
                with gzip.open(filepath, 'rb') as f:
                    compressed = True
                    out = open(re.sub(r"\.[^.]*$", "", filepath), "wb")
                    out.write(f.read())
                    out.close()
                    logs.append({"type": "text", "msg": "Decompressed gzip"})
            elif extension == "7z":
                with py7zr.SevenZipFile(filepath, 'r') as archive:
                    compressed = True
                    archive.extractall(path=re.sub(r"\.[^.]*$", "", filepath))
                    logs.append({"type": "text", "msg": "Decompressed 7zip"})
            elif extension == "tar":
                with tarfile.open(filepath, "r") as tar:
                    compressed = True
                    tar.extractall(re.sub(r"\/[^\/]*$", "", filepath))
                    logs.append({"type": "text", "msg": "Untarred"})
            else:
                return {"logs": [{"type": "download", "msg": filepath}], "newdata": [{"type": "filepath", "data": filepath}]}
            if compressed and not first:
                print("deleting " + filepath)
                os.remove(filepath)
                
            if os.path.isdir(outpath):
                for (dirpath, dirnames, filenames) in os.walk(outpath):
                    for file in filenames:
                        logs += self.return_solution(outpath + "/" + file, False, outpath)["logs"]
                    break
            else:
                logs += self.return_solution(outpath, False, outpath)["logs"]
            
            if first:
                logs.append({"type": "folder", "msg": outpath})
            if os.path.isdir(outpath):
                outdata = []
                for (dirpath, dirnames, filenames) in os.walk(outpath):
                    for file in filenames:
                        print("file: " + file)
                        outdata.append({"type": "filepath", "data": outpath + "/" + file})
            else:
                outdata = [{"type": "filepath", "data": outpath}]
            return {"logs": logs, "newdata": outdata}
        else:
            return {"logs": [], "newdata": []}