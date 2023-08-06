import os
import warnings
from datetime import datetime
from tabulate import tabulate
from pathlib import Path

import numpy as np
import numpy.lib.recfunctions as rfn

import laspy
from plyfile import PlyData, PlyElement

from matplotlib.patches import Polygon

import easyidp as idp

class PointCloud(object):

    """PointCloud class. A point cloud consists of point coordinates, and optionally point colors and point normals.
    """

    def __init__(self, pcd_path="", offset=[0.,0.,0.]) -> None:

        self.file_path = pcd_path
        self.file_ext = ".ply"

        self._points = None   # internal points with offsets to save memory
        self.colors = None
        self.normals = None
        self.shape = (0,3)

        self.offset = self._offset_type_check(offset)
        self._btf_print = '<Empty easyidp.PointCloud object>'

        if pcd_path != "":
            self.read_point_cloud(pcd_path)

    def __str__(self) -> str:
        return self._btf_print

    def __repr__(self) -> str:
        return self._btf_print

    def __len__(self) -> int:
        return self.points.shape[0]

    def _update_btf_print(self):
        """Print Point Cloud in "DataFrame" beautiful way
        >>> print(pcd)
             x    y    z  r       g       b           nx      ny      nz
        0    1    2    3  nodata  nodata  nodata  nodata  nodata  nodata
        1    4    5    6  nodata  nodata  nodata  nodata  nodata  nodata
        2    7    8    9  nodata  nodata  nodata  nodata  nodata  nodata
        """
        head = ['','x','y','z','r','g','b','nx','ny','nz']
        data = []
        col_align = ["right"] + ["decimal"]*3 + ['left']*3 + ["decimal"]*3 

        if self.shape[0] > 6:
            show_idx = [0, 1, 2, -3, -2, -1]
        else:
            show_idx = list(range(self.shape[0]))

        for i in show_idx:
            if self.has_points():
                xyz = np.around(self.points[i,:], decimals=3).tolist()
            else:
                xyz = ['nodata'] * 3

            if self.has_colors():
                rgb = self.colors[i,:].tolist()
            else:
                rgb = ['nodata'] * 3

            if self.has_normals():
                nxyz = self.normals[i,:].tolist()
            else:
                nxyz = ['nodata'] * 3
            
            if i >= 0:
                data.append([i] + xyz + rgb + nxyz)
            if i < 0:
                data.append([self.shape[0] + i] + xyz + rgb + nxyz)

        if self.shape[0] > 6:
            data.insert(3, ['...'] * 10)
            
        self._btf_print = tabulate(data, headers=head, tablefmt='plain', colalign=col_align)

    @property
    def points(self):
        if self._points is None:
            return None
        else:
            return self._points + self._offset

    @points.setter
    def points(self, p):
        if not isinstance(p, np.ndarray):
            raise TypeError(f"Only numpy ndarray object are acceptable for setting values")
        elif self.shape != p.shape and self.shape != (0,3):
            raise IndexError(f"The given shape [{p.shape}] does not match current point cloud shape [{self.shape}]")
        else:
            self._points = p - self._offset
            self.shape = p.shape
            self._update_btf_print()

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, o):
        # the point values will change:
        # --------------------------------
        # points =  _point + offset
        #   |         |         |
        # change   no change  change
        o = self._offset_type_check(o)
        self._offset = o
        if self._points is not None:
            self._update_btf_print()

    def set_offset(self, o):
        # the point values not change
        # --------------------------------
        # points =  _point + offset
        #   |         |         |
        # no change   change-   change+
        o = self._offset_type_check(o)
        
        if self._points is not None:
            self._points = self._points + self._offset - o
            self._offset = o
            warnings.warn("This will not change the value of point xyz values, if you want to just change offset value, please operate `pcd._offset = offset; pcd._update_btf_print()` directly")
            self._update_btf_print()
        else:
            self._offset = o

    @staticmethod
    def _offset_type_check(o):
        if len(o) == 3:
            if isinstance(o, (list, tuple)):
                return np.asarray(o, dtype=np.float64)
            elif isinstance(o, np.ndarray):
                return o.astype(np.float64)
            else:
                raise ValueError(f"Only [x, y, z] list or np.array([x, y, z]) are acceptable, not {type(o)} type")
        else:
            raise ValueError(f"Please give correct 3D coordinate [x, y, z], only {len(o)} was given")

    def has_colors(self):
        """Returns True if the point cloud contains point colors.

        Returns
        -------
        bool
        """
        if self.colors is None:
            return False
        else:
            return True

    def has_points(self):
        """Returns True if the point cloud contains points.

        Returns
        -------
        bool
        """
        if self._points is None:
            return False
        else:
            return True

    def has_normals(self):
        """Returns True if the point cloud contains point normals.

        Returns
        -------
        bool
        """
        if self.normals is None:
            return False
        else:
            return True

    def clear(self):
        self._points = None   # internal points with offsets to save memory
        self.colors = None
        self.normals = None
        self.shape = (0,3)

        self.offset = np.array([0.,0.,0.])

        self.file_ext = ".ply"
        self.file_path = ""

    def read_point_cloud(self, pcd_path):
        if not os.path.exists(pcd_path):
            warnings.warn(f"Can not find file [{pcd_path}], skip loading")
            return

        if Path(pcd_path).suffix == ".ply":
            points, colors, normals = read_ply(pcd_path)
        elif Path(pcd_path).suffix in [".laz", ".las"]:
            points, colors, normals = read_laz(pcd_path)
        else:
            raise IOError("Only support point cloud file format ['*.ply', '*.laz', '*.las']")

        if self.has_points():
            self.clear()

        self.file_ext = os.path.splitext(pcd_path)[-1]
        self.file_path = os.path.abspath(pcd_path)

        if abs(np.max(points)) > 65536:   # need offseting
            if not np.any(self._offset):    # not given any offset (0,0,0) -> calculate offset
                self._offset = np.floor(points.min(axis=0) / 100) * 100
            self._points = points - self._offset
        else:
            self._points = points

        self.colors = colors
        self.normals = normals
        self.shape = points.shape

        self._update_btf_print()

    def write_point_cloud(self, pcd_path):
        # if ply -> self.points + self.offsets
        # if las -> self.points & offset = self.offsets
        pcd_path = Path(pcd_path)
        file_ext = pcd_path.suffix

        if file_ext == "":
            warnings.warn(f"It seems file name [{pcd_path}] has no file suffix, using default suffix [{self.file_ext}] instead")
            out_path = pcd_path.with_name(f"{pcd_path.name}{self.file_ext}")
        else:
            if file_ext not in ['.ply', '.las', '.laz']:
                raise IOError("Only support point cloud file format ['*.ply', '*.laz', '*.las']")

            out_path = pcd_path

        if file_ext == ".ply":
            write_ply(
                self._points + self._offset, 
                self.colors, 
                ply_path=out_path, 
                normals=self.normals)
        else:
            write_laz(
                self._points + self._offset, 
                self.colors, 
                laz_path=out_path, 
                normals=self.normals, 
                offset=self._offset)

    def crop(self, roi, save_folder=None):
        """Crop several ROIs by given <ROI> object with several polygons and polygon names

        Parameters
        ----------
        roi : easyidp.ROI | dict
            the <ROI> object created by easyidp.ROI()
        is_geo : bool, optional
            whether the given polygon is pixel coords on imarray or geo coords (default)
        save_folder : str, optional
            the folder to save cropped images, use ROI indices as file_names, by default None, means not save.

        Returns
        -------
        dict,
            The dictionary with key=id and value=<idp.PointCloud>
        """
        if not self.has_points():
            raise ValueError("Could not operate when PointCloud has no points")

        if not isinstance(roi, (dict, idp.ROI)):
            raise TypeError(f"Only <dict> and <easyidp.ROI> are accepted, not {type(roi)}")

        out_dict = {}
        for k, polygon_hv in roi.items():
            if save_folder is not None and Path(save_folder).exists():
                save_path = Path(save_folder) / (k + self.file_ext)
            else:
                save_path = None

            out_dict[k] = self.crop_point_cloud(polygon_hv[:, 0:2])

            if save_path is not None:
                out_dict[k].write_point_cloud(save_path)

        return out_dict

    def crop_point_cloud(self, polygon_xy):
        """crop the point cloud along z axis

        Parameters
        ----------
        polygon_xy : nx2 ndarray
            the polygon xy coords

        Returns
        -------
        PointCloud object
            The cropped point cloud
        """

        # judge whether proper data type
        if not isinstance(polygon_xy, np.ndarray):
            raise TypeError(f"Only numpy ndarray are supported as `polygon_xy` inputs, not {type(polygon_xy)}")

        # judge whether proper shape is (N, 2)
        if len(polygon_xy.shape) != 2 or polygon_xy.shape[1] != 2:
            raise IndexError(f"Please only spcify shape like (N, 2), not {polygon_xy.shape}")

        
        # calculate the bbox of polygon
        xmin, ymin = polygon_xy.min(axis=0)
        xmax, ymax = polygon_xy.max(axis=0)

        # get the xy value if point cloud
        x = self.points[:, 0]
        y = self.points[:, 1]

        # get the row (points id) that in bbox
        inbbox_bool = (x >= xmin) * (x <= xmax) * (y >= ymin) * (y <= ymax)
        # -> array([False, False, False, ..., False, False, False])
        inbbox_idx =  np.where(inbbox_bool)[0]
        # -> array([ 3394,  3395,  3396, ..., 41371, 41372, 41373], dtype=int64)

        # filter out in bbox points
        inbbox_pts = self.points[inbbox_idx, 0:2]

        # judge by matplotlib.polygon
        plt_poly = Polygon(polygon_xy)
        in_poly_idx = plt_poly.contains_points(inbbox_pts)
        # -> array([ True, False, False, ..., False, False, False])

        # pick selected row:
        pick_idx = inbbox_idx[in_poly_idx]
        # -> array([ 3394,  3503,  3614, ..., 41265, 41285, 41369], dtype=int64)

        # check whether have data
        if len(pick_idx) > 0:
            # create new Point Cloud object
            crop_pcd = PointCloud()
            crop_pcd.points = self.points[pick_idx, :]
            crop_pcd.set_offset(self.offset)
            if self.has_colors():
                crop_pcd.colors = self.colors[pick_idx, :]
            if self.has_normals():
                crop_pcd.normals = self.normals[pick_idx, :]

            return crop_pcd
        # get empty crop
        else:
            warnings.warn("Cropped 0 point in given polygon. Please check whether the coords is correct.")
            return None


def read_ply(ply_path):
    cloud_data = PlyData.read(ply_path).elements[0].data
    ply_names = cloud_data.dtype.names

    points = np.vstack((cloud_data['x'], cloud_data['y'], cloud_data['z'])).T

    if 'red' in ply_names:
        # range in 0-255
        colors = np.vstack((cloud_data['red'], cloud_data['green'], cloud_data['blue'])).T
    elif 'diffuse_red' in ply_names:
        colors = np.vstack((cloud_data['diffuse_red'], cloud_data['diffuse_green'], cloud_data['diffuse_blue'])).T
    else:
        print(f"Can not find color info in {ply_names}")
        colors = None

    colors.dtype = np.uint8

    # read normals
    if 'nx' in ply_names:
        normals = np.vstack((cloud_data['nx'], cloud_data['ny'], cloud_data['nz'])).T
    else:
        normals = None

    return points, colors, normals


def read_las(las_path):
    """Read the las file

    Parameters
    ----------
    las_path : str
        The path to las file

    Returns
    -------
    ndarray, ndarray, ndarray
        points, colors, normals of given point cloud data
    """
    return read_laz(las_path)

def read_laz(laz_path):
    las = laspy.read(laz_path)

    points = np.vstack([las.x, las.y, las.z]).T

    # ranges 0-65536
    colors = np.vstack([las.points['red'], las.points['green'], las.points['blue']]).T / 256
    colors = colors.astype(np.uint8)

    # read normals
    """
    in cloudcompare, it locates "extended fields" -> normal x
    >>> las.point_format
    <PointFormat(2, 3 bytes of extra dims)>
    >>> las.point.array
    array([( 930206, 650950, 79707, 5654, 73, 0, 0, 0, 1, 7196,  5397, 4369, -4,  46, 118),
           ...,
           (1167278, 741188, 79668, 5397, 73, 0, 0, 0, 1, 6425,  5140, 4626, 41,  34, 114)],
          dtype=[('X', '<i4'), ('Y', '<i4'), ('Z', '<i4'), ('intensity', '<u2'), ('bit_fields', 'u1'), ('raw_classification', 'u1'), ('scan_angle_rank', 'i1'), ('user_data', 'u1'), ('point_source_id', '<u2'), ('red', '<u2'), ('green', '<u2'), ('blue', '<u2'), ('normal x', 'i1'), ('normal y', 'i1'), ('normal z', 'i1')])
    the normal type is int8 ('normal x', 'i1'), ('normal y', 'i1'), ('normal z', 'i1')
    but las.point['normal x'] -> get float value
    """
    if "normal x" in las.points.array.dtype.names:
        normals = np.vstack([las.points['normal x'], las.points['normal y'], las.points['normal z']]).T
    else:
        normals = None

    return points, colors, normals

def write_ply(points, colors, ply_path, normals=None, binary=True):
    """Save point cloud to ply format

    Parameters
    ----------
    points : ndarray
        the nx3 numpy ndarray of point XYZ info
    colors : ndarray
        the nx3 numpy ndarray of point RGB info, dtype=np.uint8
    ply_path : str
        the output point cloud file, including ext.
    normals :ndarray, optional
        the nx3 numpy ndarray of point normal info, by default None
    binary : bool, optional
        whether save the binary file.
        True: save BINARY ply file (by default)
        False: save ASCII ply file.

    Notes
    -----
    Need to convert to structured arrays [1]_ then save 
    the point cloud structure looks like this:

    .. code-block:: python

        >>> cloud_data.elements
        (PlyElement('vertex', 
            (PlyProperty('x', 'float'), 
             PlyProperty('y', 'float'), 
             PlyProperty('z', 'float'), 
             PlyProperty('red', 'uchar'), 
             PlyProperty('green', 'uchar'), 
             PlyProperty('blue', 'uchar')), count=42454, comments=[]),)
    
    convert ndarray to strucutred array [2]_ and method to merge to structured arrays [3]_

    References
    ----------
    .. [1] https://github.com/dranjan/python-plyfile#creating-a-ply-file
    .. [2] https://stackoverflow.com/questions/3622850/converting-a-2d-numpy-array-to-a-structured-array
    .. [3] https://stackoverflow.com/questions/5355744/numpy-joining-structured-arrays

    """

    # convert to strucutrre array
    struct_points = np.core.records.fromarrays(points.T, names="x, y, z")
    struct_colors = np.core.records.fromarrays(colors.T, dtype=np.dtype([('red', np.uint8), ('green', np.uint8), ('blue', np.uint8)]))

    # add normals
    if normals is not None:
        struct_normals = np.core.records.fromarrays(normals.T, names="nx, ny, nz")
        merged_list = [struct_points, struct_colors, struct_normals]
    else:
        merged_list = [struct_points, struct_colors]

    # merge 
    struct_merge = rfn.merge_arrays(merged_list, flatten=True, usemask=False)

    # convert to PlyFile data type
    el = PlyElement.describe(struct_merge, 'vertex', 
                             comments=[f'Created by EasyIDP v{idp.__version__}', 
                                       f'Created {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}'])  

    # save to file
    if binary:
        PlyData([el]).write(ply_path)
    else:
        PlyData([el], text=True).write(ply_path)

def write_laz(points, colors, laz_path, normals=None, offset=np.array([0., 0., 0.]), decimal=5):
    # create header
    header = laspy.LasHeader(point_format=2, version="1.2") 
    if normals is not None:
        header.add_extra_dim(laspy.ExtraBytesParams(name="normal x", type=np.float64))
        header.add_extra_dim(laspy.ExtraBytesParams(name="normal y", type=np.float64))
        header.add_extra_dim(laspy.ExtraBytesParams(name="normal z", type=np.float64))
    header.offsets = offset
    header.scales = np.array([float(f"1e-{decimal}")]*3)
    header.generating_software = f'EasyIDP v{idp.__version__} on {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}'

    # create las file
    las = laspy.LasData(header)

    # add values
    las.points['x'] = points[:, 0]   # here has the convert to int32 precision loss
    las.points['y'] = points[:, 1]
    las.points['z'] = points[:, 2]

    las.points['red'] = colors[:,0] * 256  # convert to uint16
    las.points['green'] = colors[:,1] * 256 
    las.points['blue'] = colors[:,2] * 256


    if normals is not None:
        las.points['normal x'] = normals[:, 0]
        las.points['normal y'] = normals[:, 1]
        las.points['normal z'] = normals[:, 2]

    las.write(laz_path)

def write_las(points, colors, las_path, normals=None, offset=np.array([0., 0., 0.]), decimal=5):
    write_laz(points, colors, las_path, normals, offset, decimal)