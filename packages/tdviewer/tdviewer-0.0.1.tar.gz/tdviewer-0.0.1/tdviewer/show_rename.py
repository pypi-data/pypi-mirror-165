from os.path import basename
import sys
import os
import json
from vis import Vis
import open3d as o3d
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R

def getFile(rootPath, ends=""):
    ret = {}
    for root, dirs, files in os.walk(rootPath):
        for filename in files:
            if filename.endswith(ends):
                tmp = {
                    "filename":filename,
                    "filepath":os.path.join(root, filename)
                }    
                ret[filename.split(".")[0]] = tmp
    
    return ret
                
def getBinPoints(binFile):
    pointsData = np.fromfile(binFile, dtype=np.float32)
    pointsData = np.delete(pointsData, 0)
    clouds = pointsData.reshape(-1, 3)
    return clouds

def strToNumList(sList):
    """
    将文件中按行读取的文件内容整理成浮点数列表
    """
    ret = []
    for i in sList:
        istr = i.strip()
        if istr == "":
            continue
        ret.append(float(istr))

    return ret


def getCar2CamParams(paramsPath):
    """
    解析车身到相机的平移旋转矩阵及内部参数矩阵
    """
    with open(paramsPath, "r") as paramfp:
        content = paramfp.read()
        contentInfo = content.split("\n")

        rotateParam = strToNumList(contentInfo[0].split(" ")) #pitch yaw roll
        transformParam = strToNumList(contentInfo[1].split(" "))
        innerParam = strToNumList(contentInfo[2].split(" "))

        R_rotvec = R.from_rotvec([rotateParam[0], rotateParam[1], rotateParam[2]])
        rotationMatrix = R_rotvec.as_matrix()
        Trans = np.array([transformParam[0], transformParam[1], transformParam[2]])[:, np.newaxis]
        extrinsic = np.concatenate((rotationMatrix, Trans), axis = 1)
        extrinsic = np.row_stack((extrinsic, np.array([0, 0, 0, 1])))

        intrinsic = np.array([
            [innerParam[0], innerParam[1], innerParam[2], 0],
            [innerParam[3], innerParam[4], innerParam[5], 0],
            [innerParam[6], innerParam[7], innerParam[8], 0],
            [0, 0, 0, 1]
        ])

    
        return extrinsic, intrinsic

def main(binPath, picPath, jsonPath, paramsPath):
    
    extrinsic, intrinsic = getCar2CamParams(paramsPath)
    
    binFileDict= getFile(binPath, ".bin")
    picFileDict = getFile(picPath, ".jpg")
    jsonFileDict = getFile(jsonPath, ".json")
    
    vis = Vis()

    plt = vis.vi

    plt.camera.SetPosition([0.0, 0.0, 171.872])
    plt.camera.SetFocalPoint([0.0, 0.0, 0.0])
    plt.camera.SetViewUp([0.0, 1.0, 0.0])
    plt.camera.SetDistance(171.872)
    plt.camera.SetClippingRange([160.122, 185.541])

    plt.size = 'fullscreen'
    
    bk = list(binFileDict.keys())
    bk.sort()
        
    for filename in bk:
        fileInfo = binFileDict[filename]
        points = getBinPoints(fileInfo["filepath"])
        
        img = cv2.imread(picFileDict[filename]["filepath"])
        
        if filename not in jsonFileDict.keys():
            continue
        
        jsonPathInfo= jsonFileDict[filename]
        
        boxs = []
        boxInfos = []
        ids = []
        with open(jsonPathInfo["filepath"], "r") as fp:
            jsonData = json.load(fp)
            for mark in jsonData[3]:
                box = np.array([mark["x"], mark["y"], mark["z"], mark["length"], mark["width"], mark["height"], mark["yaw"]])
                boxInfo = mark["type"] + "," + str(mark["id_connect"]) + "," + str(mark["id"])
                boxs.append(box)
                boxInfos.append(boxInfo)
                ids.append(int(mark["id"]))
                
                
        vis.add_3D_boxes(boxs,  ids=ids, box_info=boxInfos, caption_size=(0.09,0.09), mesh_alpha=0.3)
        vis.add_3D_cars(boxs, ids=ids, mesh_alpha=1)
        vis.set_extrinsic_mat(extrinsic)
        vis.set_intrinsic_mat(intrinsic)
        vis.add_points(points, color_map_name='viridis')
        vis.add_image(img)
        vis.show_3D()
        vis.show_2D()

if __name__ == "__main__":
    binPath = sys.argv[1]
    picPath = sys.argv[2]
    jsonPath = sys.argv[3]
    paramsPath = sys.argv[4]
    main(binPath, picPath, jsonPath, paramsPath)