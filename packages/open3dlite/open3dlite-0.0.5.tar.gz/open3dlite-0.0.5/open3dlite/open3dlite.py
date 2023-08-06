import open3d as o3d
from open3d import *
import numpy as np


def from_numpy(np_array, colors = None, color = False):
    r, c = np.shape(np_array)
    if r != c and (r == 3):
        np_array = np_array.T
    if r != 3 and c != 3:
        raise Exception("Dimentions of numpy array is incorrect")
    pcd = o3d.geometry.PointCloud()
    if color:
        pcd.colors = o3d.utility.Vector3dVector(np_array)
    else:
        pcd.points = o3d.utility.Vector3dVector(np_array)
    if colors is not None:
        add_colors(colors)
    
    return pcd


def add_colors(np_array):
    from_numpy(np_array, None, color = True)

def to_numpy(pcd):
    return np.asarray(pcd.points)

def colors(pcd):
    return np.asarray(pcd.colors)

def write(name, pcd):
    o3d.io.write_point_cloud(name, pcd)


def read(path):
    return o3d.io.read_point_cloud(path)


def show(*pcls):
    if type(pcls[0]) == type([]):
        pcl_list = pcls[0]
    else:
        pcl_list = list(pcls)
    o3d.visualization.draw_geometries(pcl_list)

