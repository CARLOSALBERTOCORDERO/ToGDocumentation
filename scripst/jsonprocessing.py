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
    print("Images found: {}".format(metadataList))
    metadataDictProcessed = dict()
    for metadataElement in range(0,metadataNum):
        metadataName = metadataList[metadataElement].split(os.sep)[-1]
        with open(metadataList[metadataElement], 'r') as f:
            metadata_dict = json.load(f)
        metadataDictProcessed["GSD"] = float(metadata_dict["gsd"])
        metadataDictProcessed["CloudCover"] = float(metadata_dict["cloud_cover"])
        metadataDictProcessed["OffNadirAngle"] = float(metadata_dict["off_nadir_angle_dbl"])
        utm = metadata_dict["utm"]
        utmNum = utm[:2]
        utmLetter = utm[-1:]
        logitude = (float(utmNum) - 30) * 6
        latitude = (ord(utmLetter) - ord('M')) * 8
        metadataDictProcessed["Longitude_x"] = math.cos(math.radians(logitude))
        metadataDictProcessed["Longitude_y"] = math.sin(math.radians(logitude))
        metadataDictProcessed["Latitude_z"] = math.sin(math.radians(latitude))
        date, time = metadata_dict["timestamp"].split("T")
        yy, mm, dd = date.split("-")
        time = time[:-1]
        hh, min, ss = time.split(":")
        metadataDictProcessed["Year"] = float(yy)
        metadataDictProcessed["Month"] = float(mm)
        metadataDictProcessed["Day"] = float(dd)
        metadataDictProcessed["HourMinute"] = float(hh) + (float(min)/100)
        sun_az = float(metadata_dict["sun_azimuth_dbl"])
        metadataDictProcessed["SunAzimuthAngle_x"] = math.cos(math.radians(sun_az))
        metadataDictProcessed["SunAzimuthAngle_y"] = math.sin(math.radians(sun_az))
        metadataDictProcessed["SunElevationAngle"] = float(metadata_dict["sun_elevation_dbl"])
        tar_az = float(metadata_dict["target_azimuth_dbl"])
        metadataDictProcessed["TargetAzimuthAngle_x"] = math.cos(math.radians(tar_az))
        metadataDictProcessed["TargetAzimuthAngle_y"] = math.sin(math.radians(tar_az))
        metadataDictProcessed["LocalHour"] = metadataDictProcessed["HourMinute"] + (float(utmNum) - 30)
        if(24 < metadataDictProcessed["LocalHour"]):
            metadataDictProcessed["LocalHour"] = metadataDictProcessed["LocalHour"] - 24
        elif(0 > metadataDictProcessed["LocalHour"]):
            metadataDictProcessed["LocalHour"] = metadataDictProcessed["LocalHour"] + 24 
        else:
            pass            
        metadataDictProcessed["WeekDay"] = datetime.date(int(yy),int(mm),int(dd)).weekday()
        metadataDictProcessed["BoundingBoxes"] = len(metadata_dict["bounding_boxes"])
        width = metadata_dict["bounding_boxes"][0]["box"][3] - metadata_dict["bounding_boxes"][0]["box"][1]
        height = metadata_dict["bounding_boxes"][0]["box"][2] - metadata_dict["bounding_boxes"][0]["box"][0]
        metadataDictProcessed["OriginalBoundingBoxWidth"] = math.log10(width)
        metadataDictProcessed["OriginalBoundingBoxHeight"] = math.log10(height)
        metadataDictProcessed["BoundingBoxAspectRatio_log"] = math.log10(width/height)
        metadataDictProcessed["Box2ImageWidthRatio"] = width/float(metadata_dict["img_width"])
        metadataDictProcessed["Box2ImageHeightRatio"] = height/float(metadata_dict["img_height"])
        metadataDictProcessed["Box2ImageRatio"] = (width*height) / (metadata_dict["img_width"]*metadata_dict["img_height"])
        
        
    print(metadataDictProcessed)


if __name__ == "__main__":
    main()