from types import NoneType
import open3d as o3d
from open3d import *
import numpy as np

class Pcl():

    def __init__(self):
        self.pcd = None
    
    def read(self, path):
        self.pcd = o3d.io.read_point_cloud(path)
        
    def show(self):
        o3d.visualization.draw_geometries([self.pcd])
    
    def from_numpy(self, np_array, colors = None, _color = False):
        r, c = np.shape(np_array)
        if r != c and (r == 3):
            np_array = np_array.T
        if r != 3 or c != 3:
            raise Exception("Dimentions of numpy array is incorrect")
        if self.pcd is None:
            self.pcd = o3d.geometry.PointCloud()
        if _color:
            self.pcd.colors = o3d.utility.Vector3dVector(np_array)
        else:
            self.pcd.points = o3d.utility.Vector3dVector(np_array)
        if colors is not None:
            self.add_colors(colors)


    def add_colors(self, np_array):
        self.from_numpy(np_array, None, _color = True)

    def to_numpy(self):
        return np.asarray(self.pcd.points)

    def colors(self):
        return np.asarray(self.pcd.colors)

    def write(self, name):
        o3d.io.write_point_cloud(name, self.pcd)


def read(path):
    pcl = Pcl()
    pcl.pcl = o3d.io.read_point_cloud(path)
    return pcl


def show(pcls):
    pcl_list = []
    for pcl in pcls:
        pcl_list.append(pcl.pcd)
    o3d.visualization.draw_geometries(pcl_list)

def from_numpy(np_array):
    pcl = Pcl()
    pcl.from_numpy(np_array)
    return pcl