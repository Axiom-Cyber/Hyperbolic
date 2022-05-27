import matplotlib.pyplot as plt
from os import path
from PIL import Image
import numpy as np

def renderImage(pathName, outName, width):
    outName = outName.replace(".png", "")
    file=open(pathName, "rb")
    size = (path.getsize(pathName) / 4) - 4

    if width == "guess":
        widths = []
        for width in range(50, int(size)-50):
            if (size/width) % 1 == 0 and size/(width**2) > 0.25 and size/(width**2) < 4:
                widths.append(width)

    else:
        widths = [int(width)]
    
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
        Image.fromarray(outArray).save(outName+str(width)+".png")

    file.close()

if __name__ == "__main__":
    renderImage("C:\\Users\\clemevin000\\Downloads\\flag.data", "C:\\Users\\clemevin000\\Downloads\\out.png", "guess")