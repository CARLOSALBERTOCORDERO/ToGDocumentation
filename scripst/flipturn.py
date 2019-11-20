import json
import __main__
import os
from PIL import Image
import shutil
import matplotlib.pyplot as plt
import numpy as np
import PIL

def getImageList(dbPath):
    returnImageList = list()
    returnMetadataList = list()
    elementsNum = 0
    for root, dirs, files in os.walk(dbPath, topdown=False):
        for fileName in files:
            if(-1 != fileName.find("msrgb.jpg")):
                returnImageList.append(os.path.join(root, fileName))
                elementsNum = elementsNum + 1
            if(-1 != fileName.find("msrgb.json")):
                returnMetadataList.append(os.path.join(root, fileName))
        for dirName in dirs:
            #print(os.path.join(root, dirName))
            pass
    return (returnImageList,returnMetadataList, elementsNum)

def main():
    currentPath = os.getcwd()
    auxPathStr = ""
    auxPathList = list()
    dbPath = currentPath + os.sep + "ToGDatabaseRotFlip"
    (imageList, metadataList, elements) = getImageList(dbPath)
    for imageFile in imageList:
        im = Image.open(imageFile)
        auxPathList = list()
        #flip image
        imIn = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        auxPathList = imageFile.split(".")
        auxPathStr = auxPathList[0] + "_f." + auxPathList[1]
        out_file = open( auxPathStr, 'wb' )
        imIn.save(auxPathStr)
        out_file.flush()
        out_file.close()
        out = imIn.rotate(90)
        auxPathList = imageFile.split(".")
        auxPathStr = auxPathList[0] + "_f90." + auxPathList[1]
        out_file = open( auxPathStr, 'wb' )
        out.save(auxPathStr)
        out_file.flush()
        out_file.close()
        out1 = imIn.rotate(180)
        auxPathList = imageFile.split(".")
        auxPathStr = auxPathList[0] + "_f180." + auxPathList[1]
        out_file = open( auxPathStr, 'wb' )
        out1.save(auxPathStr)
        out_file.flush()
        out_file.close()
        out2 = imIn.rotate(270)
        auxPathList = imageFile.split(".")
        auxPathStr = auxPathList[0] + "_f270." + auxPathList[1]
        out_file = open( auxPathStr, 'wb' )
        out2.save(auxPathStr)
        out_file.flush()
        out_file.close()


if __name__ == "__main__":
    main()