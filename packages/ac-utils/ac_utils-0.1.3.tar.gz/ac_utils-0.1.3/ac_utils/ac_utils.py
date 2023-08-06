"""
Functions for working with robotics.
"""

__docformat__ = "restructuredtext en"

import numpy as np
from numpy.lib import recfunctions as rfn
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
from builtin_interfaces.msg import Time
from scipy.spatial.transform import Rotation
import cupy as cp

# dics of types exchanges between PointField and numpy
_PFTYPE_TO_NPTYPE = {
    PointField.INT8: np.int8,
    PointField.UINT8: np.uint8,
    PointField.INT16: np.int16,
    PointField.UINT16: np.uint16,
    PointField.INT32: np.int32,
    PointField.UINT32: np.uint32,
    PointField.FLOAT32: np.float32,
    PointField.FLOAT64: np.float64
}
_NPTYPE_TO_PFTYPE = {v: k for k, v in _PFTYPE_TO_NPTYPE.items()}


def _fields_to_dtype(point_fields, point_step):
    """
    Transform PointCloud2.fields to np.dtype & list[Fields name]

    Parameters
    ----------
    point_fields : sequence<sensor_msgs/PointField>
        PointCloud2.fields
    point_step : int
        PointCloud2.point_step

    Returns
    -------
    fields_dtype : np.dtype
        PointFields as np.dtype
    fields_name: list[str]
        List of PointFields name

    Examples
    --------
    >> _fields_to_dtype(sequence<sensor_msgs/PointField>, 12)
    {'names': ['x', 'y', 'z'], 'formats': ['<f4', '<f4', '<f4'], 'offsets': [0, 4, 8], 'itemsize': 12}, ['x', 'y', 'z']
    """

    dtypes_names = []
    dtypes_formats = []
    dtypes_offsets = []

    for field in point_fields:
        dtypes_names.append(field.name)
        dtypes_formats.append(_PFTYPE_TO_NPTYPE.get(field.datatype))
        dtypes_offsets.append(field.offset)
    fields_name = dtypes_names[:]

    # Tail-Padding
    padding_offset = dtypes_offsets[-1] + np.dtype(dtypes_formats[-1]).itemsize
    if padding_offset < point_step:
        dtypes_names.append('padding')
        dtypes_formats.append(np.dtype(f'V{point_step-padding_offset}'))
        dtypes_offsets.append(padding_offset)

    return np.dtype({'names': dtypes_names, 'formats': dtypes_formats, 'offsets': dtypes_offsets}), fields_name


def _field_generator(fields_name_nptype):
    """
    Create a list of PointFields by names & nptype

    Parameters
    ----------
    fields_name_nptype : np.array([[str, np.dtype]])
        np.Array of PointFields name and nptype

    Returns
    -------
    fields : list[PointField]
        List of PointFields

    Examples
    --------
    >> _field_generator(['x', 'y', 'z'], [np.float32, np.float32, np.float32])
    sequence<sensor_msgs/PointField>
    """

    fields = []
    offset = 0
    for i in range(fields_name_nptype.shape[0]):
        fields.append(PointField(
            name=fields_name_nptype[i, 0],
            offset=offset,
            datatype=_NPTYPE_TO_PFTYPE.get(fields_name_nptype[i, 1]),
            count=1  # Assumption
        ))
        offset += np.dtype(fields_name_nptype[i, 1]).itemsize

    return fields


def pointcloud2_to_array(pointcloud2, specified_fields=None):
    """
    Transform a PointCloud2 to np.array shape(nº points, nº fields)

    Parameters
    ----------
    pointcloud2 : PointCloud2
        PointCloud2 msg
    specified_fields : list[str], optional
        List of fields to extract

    Returns
    -------
    pointcloud : np.array
        Array of points shape(nº points, nº fields)

    Examples
    --------
    >> pointcloud2_to_array(pointcloud2, ['x', 'y', 'z'])
    array([[0., 0., 0.],
           [5., 4., 9.]])
    """

    fields_dtype, fields_name = _fields_to_dtype(pointcloud2.fields, pointcloud2.point_step)

    # Removing padding field & Converting to numpy.ndarray
    return rfn.structured_to_unstructured(np.frombuffer(pointcloud2.data, fields_dtype)[
                                              fields_name if specified_fields is None
                                              else specified_fields
                                          ])


def array_to_pointcloud2(pointcloud, fields_name_nptype, stamp=Time(), frame_id=''):
    """
    Transform a np.array shape(nº points, nº fields) to a PointCloud2 msg

    Parameters
    ----------
    pointcloud : np.array
        Array of points shape(nº points, nº fields)
    fields_name_nptype : np.array([[str, np.dtype]])
        List of tuples of fields name and np.dtype of pointcloud
    stamp : Time(), optional
        stamp
    frame_id : str, optional
        frame_id

    Returns
    -------
    pointcloud2 : PointCloud2
        PointCloud2 msg

    Examples
    --------
    >> array_to_pointcloud2(np.array([[0., 0., 0.],[5., 4., 9.]]), ['x', 'y', 'z'], [np.float32, np.float32, np.float32])
    PointCloud2
    """
    data = rfn.unstructured_to_structured(
        pointcloud,
        np.dtype({'names': fields_name_nptype[:, 0], 'formats': fields_name_nptype[:, 1]})
    )

    return PointCloud2(
        header=Header(
            stamp=stamp,
            frame_id=frame_id
        ),
        height=1,  # Assumption
        width=data.shape[0],
        fields=_field_generator(fields_name_nptype),
        is_bigendian=False,  # Assumption
        point_step=data.dtype.itemsize,
        row_step=data.shape[0]*data.dtype.itemsize,
        data=data.tobytes(),
        is_dense=True  # Assumption
    )


def get_transform_matrix(transform):
    rotation_matrix = Rotation.from_quat([
        transform.transform.rotation.x,
        transform.transform.rotation.y,
        transform.transform.rotation.z,
        transform.transform.rotation.w
    ]).as_matrix()
    translation_vector = [
        transform.transform.translation.x,
        transform.transform.translation.y,
        transform.transform.translation.z
    ]
    return np.vstack((np.c_[rotation_matrix, translation_vector], [0., 0., 0., 1.]))


# https://github.com/ros2/geometry2/blob/ros2/tf2_sensor_msgs/tf2_sensor_msgs/tf2_sensor_msgs.py
def affine_transform(pointcloud, transform_matrix):
    pointcloud[:, :3] = np.matmul(transform_matrix, np.c_[pointcloud[:, :3], np.ones(pointcloud.shape[0])].T).T[:, :3]
    # pointcloud[:, :3] = np.matmul(transform_matrix, np.r_[pointcloud[:, :3].T, np.ones((1, pointcloud.shape[0]))])[:3].T
    return pointcloud


def cp_affine_transform(pointcloud, transform_matrix):
    pointcloud[:, :3] = cp.asnumpy(cp.matmul(
        cp.asarray(transform_matrix),
        cp.asarray(np.r_[pointcloud[:, :3].T, np.ones((1, pointcloud.shape[0]))])
    )[:3].T)

    return pointcloud


def _roi_points_mask(pointcloud, roi):
    return (roi[0][0] <= pointcloud[:, 0]) & (pointcloud[:, 0] <= roi[1][0]) & \
           (roi[0][1] <= pointcloud[:, 1]) & (pointcloud[:, 1] <= roi[1][1]) & \
           (roi[0][2] <= pointcloud[:, 2]) & (pointcloud[:, 2] <= roi[1][2])


def get_roi_points(pointcloud, roi):
        roi_points_mask = _roi_points_mask(pointcloud=pointcloud, roi=roi)

        return pointcloud[roi_points_mask], roi_points_mask


def uniform_grid_sampling(pointcloud, grid_dim, resolution):
    y = [grid_dim[0], grid_dim[1]]
    # 1. Calcular coordenadas
    grid_sampling = np.floor((pointcloud[:, :2]-y)/resolution)
    # 2. Calcular hash
    pointcloud_ids = np.matmul([np.ceil(np.linalg.norm(grid_dim[3]-grid_dim[1])/resolution), 1.], grid_sampling.T)
    # 3. Eliminar duplicados
    grid_points_ids, grid_points_ids_index = np.unique(pointcloud_ids, axis=0, return_index=True)
    # 4. reubicar
    grid_points = grid_sampling.take(grid_points_ids_index, axis=0) * resolution + y

    return pointcloud_ids, grid_points, grid_points_ids


def _groupby(dataset, labels):
    sorted_indices = np.argsort(labels)
    sorted_dataset = dataset[sorted_indices]
    sorted_label = labels[sorted_indices]
    slices_start_indice = np.r_[0, np.flatnonzero(np.diff(sorted_label)) + 1]

    return sorted_dataset, slices_start_indice


def grouped_minmax(dataset, labels):
    if dataset.shape[0] == labels.shape[0] and labels.shape[0]:
        sorted_dataset, slices_start_indice = _groupby(dataset, labels)

        return np.c_[
            np.minimum.reduceat(sorted_dataset, slices_start_indice, axis=0),
            np.maximum.reduceat(sorted_dataset, slices_start_indice, axis=0)
        ]
    else:
        return np.empty(shape=0)


def grounded_bounding_boxes(pointcloud, labels):
    if pointcloud.shape[0] == labels.shape[0] and labels.shape[0]:
        sorted_dataset, slices_start_indice = _groupby(pointcloud, labels)

        return np.c_[
            np.minimum.reduceat(sorted_dataset[:, :2], slices_start_indice, axis=0),
            np.maximum.reduceat(sorted_dataset, slices_start_indice, axis=0)
        ]
    else:
        return np.empty(shape=0)
