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


def main(binPath, jsonPath):
    binFileDict= getFile(binPath, ".pcd")
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
        print(filename)
        pcd = o3d.io.read_point_cloud(binFileDict[filename]["filepath"])
        points = np.asarray(pcd.points)
        jsonPathInfo= jsonFileDict[filename]
        

        with open(jsonPathInfo["filepath"], "r") as fp:
            jsonData = json.load(fp)
            for mark in jsonData["objects"]:
                box = np.array([float(mark["x"]), float(mark["y"]), float(mark["z"]), float(mark["length"]), float(mark["width"]), float(mark["height"]), float(mark["yaw"])])
                boxInfo = mark["type"] + "," + str(mark["id_connect"]) + "," + str(mark["id"])
                vis.add_3D_boxes([box],  ids=[int(mark["id"])], box_info=boxInfo, caption_size=(0.09,0.09), mesh_alpha=0.3)
                # vis.add_3D_cars([box], ids=[int(mark["id"])], mesh_alpha=1)
        
        vis.add_points(points, color_map_name='viridis')
        vis.show_3D()

if __name__ == "__main__":
    binPath = sys.argv[1]
    jsonPath = sys.argv[2]
    main(binPath, jsonPath)