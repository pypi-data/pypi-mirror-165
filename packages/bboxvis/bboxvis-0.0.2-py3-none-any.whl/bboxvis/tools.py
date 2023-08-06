import numpy as np
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.spatial import ConvexHull
from copy import copy, deepcopy
import numba

def get_corners(bbox, ret_center=False):
    '''
    bbox format: [x,y,z,l,w,h,yaw]
    coordinate frame:
    +z
    |
    |
    ----- +y
    \
     \
      +x

    Corner numbering::
         5------4
         |\     |\
         | \    | \
         6--\---7  \
          \  \   \  \
     l     \  1------0    h
      e     \ |    \ |    e
       n     \|     \|    i
        g     2------3    g
         t      width     h
          h               t

    First four corners are the ones facing front.
    The last four are the ones facing back.
    '''
    l, w, h = bbox[3:6]
    #                      front           back
    xs = l/2 * np.array([1, 1, 1, 1] + [-1,-1,-1,-1])
    ys = w/2 * np.array([1,-1,-1, 1] * 2)
    zs = h/2 * np.array([1, 1,-1,-1] * 2)
    pts = np.vstack([xs, ys, zs])       # (3, 8)

    center = bbox[:3]
    yaw = bbox[6]
    R = Rotation.from_euler('z', yaw).as_matrix()   # (3, 3)
    pts = (R @ pts).T + center
    if ret_center == True:
        return pts, center
    return pts

def get_visual_lines(bbox, color='r', width=1):
    from vispy.scene import visuals

    pts = get_corners(bbox)
    connect = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0],  # front
        [4, 5], [5, 6], [6, 7], [7, 4],  # back
        [0, 4], [1, 5], [2, 6], [3, 7],  # side
        [0, 2], [1, 3], # front cross
    ])
    lines = visuals.Line(pos=pts, connect=connect, color=color, width=width,
                         antialias=True, method='gl')
    return lines

def get_visual_arrows(bbox, color='g', width=1):
    from vispy.scene import visuals
    center = bbox[:3]
    pts = get_corners(bbox)
    front_center = (pts[0] + pts[1]) / 2
    connect = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0],  # front
        [4, 5], [5, 6], [6, 7], [7, 4],  # back
        [0, 4], [1, 5], [2, 6], [3, 7],  # side
        [0, 2], [1, 3], # front cross
    ])
    return visuals.Line.arrow.ArrowVisual(pos=pts, connect=connect, color=color, width=width, 
                        method='gl', antialias=True)
def pc_in_box(box, pc, box_scaling=1, mask=False):
    center_x, center_y, center_z, length, width, height = box[0:6]
    yaw = box[6]
    if mask == False:
        return pc_in_box_inner(center_x, center_y, center_z, length, width, height, yaw, pc, box_scaling)
    else:
        return pc_in_box_inner_mask(center_x, center_y, center_z, length, width, height, yaw, pc, box_scaling)


@numba.njit
def pc_in_box_inner(center_x, center_y, center_z, length, width, height, yaw, pc, box_scaling=1):
    mask = np.zeros(pc.shape[0], dtype=np.int32)
    ndims = pc.shape[1]
    yaw_cos, yaw_sin = np.cos(yaw), np.sin(yaw)
    for i in range(pc.shape[0]):
        rx = np.abs((pc[i, 0] - center_x) * yaw_cos +
                    (pc[i, 1] - center_y) * yaw_sin)
        ry = np.abs((pc[i, 0] - center_x) * -yaw_sin +
                    (pc[i, 1] - center_y) * yaw_cos)
        rz = np.abs(pc[i, 2] - center_z)

        if rx < (length * box_scaling / 2) and ry < (width * box_scaling / 2) and rz < (height * box_scaling / 2):
            mask[i] = 1
    indices = np.argwhere(mask == 1)
    result = np.zeros((indices.shape[0], ndims), dtype=np.float64)
    for i in range(indices.shape[0]):
        result[i, :] = pc[indices[i], :]
    return result


@numba.njit
def pc_in_box_inner_mask(center_x, center_y, center_z, length, width, height, yaw, pc, box_scaling=1):
    mask = np.zeros(pc.shape[0], dtype=np.int32)
    yaw_cos, yaw_sin = np.cos(yaw), np.sin(yaw)
    for i in range(pc.shape[0]):
        rx = np.abs((pc[i, 0] - center_x) * yaw_cos +
                    (pc[i, 1] - center_y) * yaw_sin)
        ry = np.abs((pc[i, 0] - center_x) * -yaw_sin +
                    (pc[i, 1] - center_y) * yaw_cos)
        rz = np.abs(pc[i, 2] - center_z)

        if rx < (length * box_scaling / 2) and ry < (width * box_scaling / 2) and rz < (height * box_scaling / 2):
            mask[i] = 1
    indices = np.argwhere(mask == 1)
    return indices

@numba.njit
def downsample(points, voxel_size=0.05):
    sample_dict = dict()
    for i in range(points.shape[0]):
        point_coord = np.floor(points[i] / voxel_size)
        sample_dict[(int(point_coord[0]), int(point_coord[1]), int(point_coord[2]))] = True
    res = np.zeros((len(sample_dict), 3), dtype=np.float32)
    idx = 0
    for k, v in sample_dict.items():
        res[idx, 0] = k[0] * voxel_size + voxel_size / 2
        res[idx, 1] = k[1] * voxel_size + voxel_size / 2
        res[idx, 2] = k[2] * voxel_size + voxel_size / 2
        idx += 1
    return res

def pca(points):
    '''
    Args
    -----
        points: np.ndarray, shape (N, 3)
    Return
    ------
        mu, covariance, eigen_value, eigen_vector
    '''
    pts_num = points.shape[0]
    mu = np.mean(points, axis=0)
    normalized_points = points - mu
    covariance = (1/pts_num - 1) * normalized_points.T @ normalized_points
    eigen_vals, eigen_vec = np.linalg.eig(covariance)
    return mu, covariance, eigen_vals, eigen_vec