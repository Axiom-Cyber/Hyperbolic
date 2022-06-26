import matplotlib.pyplot as plt
from os import path
import os
from PIL import Image
import numpy as np
import re
import hyperbola
import filetype

@hyperbola.Commander.add_worker('filepath')
class RenderBinary:
    def return_solution(self, pathName):
        outName = re.sub(r"\.[^.]*$", "", pathName)
        file=open(pathName, "rb")
        size = (path.getsize(pathName) / 4) - 4
        widths = []
        for width in range(50, int(size)-50):
            if (size/width) % 1 == 0 and size/(width**2) > 0.25 and size/(width**2) < 4:
                widths.append(width)
        
        if len(widths) > 0: 
            os.makedirs(outName)
        for width in widths:
            file.seek(0)
            pixels = []
            for i in range(int(size/width)):
                row = []
                for j in range(width):
                    color = file.read(4)
                    row.append(tuple(int(k) for k in color))
                pixels.append(row)
            
            outArray = np.array(pixels, dtype=np.uint8)
            Image.fromarray(outArray).save(outName + "/" + str(width) + ".png")

        file.close()
        return {'logs': [],'newdata':[{"type":"filepath", "data":outName}],'end':False}
