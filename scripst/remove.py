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
        if((-1 == imageFile.find("_f.")) and (-1 == imageFile.find("_f90")) and (-1 == imageFile.find("_f180")) and (-1 == imageFile.find("_f270"))):
            #print(imageFile)
            os.remove(imageFile)

if __name__ == "__main__":
    main()