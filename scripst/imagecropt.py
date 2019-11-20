import json
import __main__
import os
from PIL import Image
import shutil

def cropImages(imagesList, metadataList, imageNum, destPath):
    folderList = os.listdir(destPath)
    folderList.remove(".git")
    folderFoud = False
    folderIndex = 0
    destDir = ""
    imageName = ""
    metadataName = ""
    numPixels = 0
    for imageIndex in range(0,imageNum):
        imageName = imagesList[imageIndex].split(os.sep)[-1]
        metadataName = metadataList[imageIndex].split(os.sep)[-1]
        with open(metadataList[imageIndex], 'r') as f:
            metadata_dict = json.load(f)
        numPixels = metadata_dict["bounding_boxes"][0]["box"][2] - metadata_dict["bounding_boxes"][0]["box"][0]
        numPixels *= metadata_dict["bounding_boxes"][0]["box"][3] - metadata_dict["bounding_boxes"][0]["box"][1]
        if(40 > metadata_dict["cloud_cover"]) and (5 < numPixels):
            #print("bounding box:")
            #print(metadata_dict["bounding_boxes"][0]["box"])
            image = cropImage(imagesList[imageIndex], metadata_dict["bounding_boxes"][0]["box"])
            folderFoud = False
            folderIndex = 0
            destDir = ""
            while(False == folderFoud):
                if( -1 != imagesList[imageIndex].find(folderList[folderIndex])):
                    folderFoud = True
                    destDir = folderList[folderIndex]
                else:
                    folderIndex = folderIndex + 1
            #print(os.path.join(destPath, destDir) + os.sep + imageName)
            image.save(os.path.join(destPath, destDir) + os.sep + imageName)
            shutil.copy(metadataList[imageIndex], os.path.join(destPath, destDir) + os.sep + metadataName)    
        else:
            print(imagesList[imageIndex])

def cropImage(imagePath, boundingBoxList):
    dimention = 224
    left = boundingBoxList[0]
    top = boundingBoxList[1]
    right = boundingBoxList[2]
    bottom = boundingBoxList[3]
    leftDBbox = 0
    topDBbox = 0
    rightDBbox = 0
    bottomDBbox = 0
    
    imageCenter = ((((right - left)/2) + left), \
        (((bottom - top)/2) + top))
    #print(imagePath)
    im = Image.open(imagePath)
    #im.show()
    imCrop = im.crop((left, top, right, bottom)) 
    #imCrop.show()
    leftDBbox = imageCenter[0] - (dimention/2)
    topDBbox = imageCenter[1] - (dimention/2)
    rightDBbox = imageCenter[0] + (dimention/2)
    bottomDBbox = imageCenter[1] + (dimention/2)
    imDBCrop = im.crop((leftDBbox, topDBbox, rightDBbox, bottomDBbox)) 
    #imDBCrop.show()
    return imDBCrop

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

def angarTerminalCopy(destPathIn):
    originPath = ""
    destPath = ""
    for root, dirs, files in os.walk(destPathIn, topdown=False):
        for fileName in files:
            if(-1 != fileName.find("airport_hangar")):
                originPath = os.path.join(root, fileName)
                destPath = destPathIn + os.sep + "airport_hangar" + \
                os.sep + fileName
                shutil.move(originPath, destPath)
            if(-1 != fileName.find("airport_terminal")):
                originPath = os.path.join(root, fileName)
                destPath = destPathIn + os.sep + "airport_terminal" + \
                os.sep + fileName
                shutil.move(originPath, destPath)

def main():
    currentPath = os.getcwd()
    imagesList = list()
    metadataList = list()
    imagesNum = 0
    dbPath = ""
    destPath = ""
    auxPathlist = list()
    
    #Obtain DB path
    dbPath = currentPath + os.sep + "tesis" + os.sep + "dataset"\
        + os.sep + "fMoW-rgb_trainval_v1.0.0.tar" + os.sep +\
        "fMoW-rgb_trainval_v1.0.0" + os.sep + "fMoW-rgb" + os.sep\
        + "train"
    
    #Create destination folders
    destPath = currentPath + os.sep + "ToGDatabase"
    auxPathlist = os.listdir(dbPath)
    #for dir in auxPathlist:
    #    os.mkdir(os.path.join(destPath, dir))
    
    print("DB path: " + dbPath)
    (imagesList, metadataList, imagesNum) = getImageList(dbPath)
    print("Images found: {}".format(imagesNum))
    cropImages(imagesList, metadataList, imagesNum, destPath)
    #angarTerminalCopy(destPath)



if __name__ == "__main__":
    main()