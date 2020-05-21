import json
import __main__
import os
from PIL import Image
import shutil
import math
import datetime


def getMetadataList(dbPath):
    returnImageList = list()
    returnMetadataList = list()
    elementsNum = 0
    for root, dirs, files in os.walk(dbPath, topdown=False):
        for fileName in files:
            if(-1 != fileName.find("msrgb.json")):
                returnMetadataList.append(os.path.join(root, fileName))
                elementsNum = elementsNum + 1
        for dirName in dirs:
            #print(os.path.join(root, dirName))
            pass
    return (returnImageList,returnMetadataList, elementsNum)


def main():
    currentPath = os.getcwd()
    imagesList = list()
    metadataList = list()
    imagesNum = 0
    dbPath = ""
    destPath = ""
    auxPathlist = list()
    
    #Obtain DB path
    dbPath = currentPath
    
    #Create destination folders
    destPath = currentPath + os.sep + "ToGDatabase"
    auxPathlist = os.listdir(dbPath)

    print("DB path: " + dbPath)
    (imagesList, metadataList, metadataNum) = getMetadataList(dbPath)
    metadataDictProcessed = dict()
    for metadataElement in range(0,metadataNum):
        metadataName = metadataList[metadataElement].split(os.sep)[-1]
        with open(metadataList[metadataElement], 'r') as f:
            metadata_dict = json.load(f)
        metadataDictProcessed["BoundingBoxes"] = len(metadata_dict["bounding_boxes"])
        if(1 < metadataDictProcessed["BoundingBoxes"]):
            print(metadataList[metadataElement])



if __name__ == "__main__":
    main()