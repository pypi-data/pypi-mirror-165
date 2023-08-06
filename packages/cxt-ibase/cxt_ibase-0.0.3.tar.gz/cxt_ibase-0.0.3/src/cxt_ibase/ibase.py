import os.path
import sys
from operator import mul
from functools import reduce

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from sklearn.preprocessing import StandardScaler


class standard:

    def __init__(self, data, features):
        if not isinstance(features, list) and not isinstance(features, tuple):
            features = [features]
        self.features = features # position for features
        self.data_shape = data.shape
        self.features_num = reduce(mul, (data.shape[c] for c in features))
        self.list_t = self.transpose_list(data.shape, features)
        self.scale = StandardScaler().fit(self.reshape(data)[0])
        pass

    def reshape(self, data):
        data = data.reshape((-1, ) + self.data_shape[1:])
        data_transpose = data.transpose(self.list_t)
        return data_transpose.reshape((-1, self.features_num)), data_transpose.shape

    def transform(self, data):
        data_reshape, data_transposedshape = self.reshape(data)
        data_scaled = self.scale.transform(data_reshape).reshape(data_transposedshape).transpose(self.list_t)
        return data_scaled

    def inverse_transform(self, data):
        data_reshape, data_transposedshape = self.reshape(data)
        data_inverse = self.scale.inverse_transform(data_reshape).reshape(data_transposedshape).transpose(self.list_t)
        return data_inverse

    def transpose_list(self, data_shape, features):
        features_transpose = list(features)
        position = list(range(len(data_shape) - len(features), len(data_shape)))
        position_transpose = list(position)
        for c in features:
            if c in position:
                features_transpose.remove(c)
                position_transpose.remove(c)
        ilist = list(range(len(data_shape)))
        for f, p in zip(features_transpose, position_transpose):
            ilist[f], ilist[p] = ilist[p], ilist[f]
        return ilist

def filename_py(filename):

    filename = os.path.basename(filename)
    return filename.split('.py')[0]


class TimeC:
    def clock(func):
        from time import time

        def clocked(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            end = time()
            name = func.__name__
            print('{}: {}'.format(name, end - start))
            return result
        return clocked


def meshgrid(*args):
    shape = ()
    for c in args:
        shape += c.shape
    result = np.meshgrid(*args, indexing='ij')
    for c in result:
        yield c.reshape(shape)


def shuffle(*args, axis=0):
    # shuffle arrays in dimension of axis
    n = args[0].shape[axis]
    shuffle_shape = np.arange(n)
    np.random.shuffle(shuffle_shape)
    for arr in args:
        transpose_shape = np.arange(len(arr.shape))
        transpose_shape[0], transpose_shape[axis] = axis, 0
        arr_temp = np.array(arr)
        arr_transpose = arr_temp.transpose(transpose_shape)
        arr_transpose_shuffle = arr_transpose[shuffle_shape]
        arr_transpose2 = arr_transpose_shuffle.transpose(transpose_shape)
        yield arr_transpose2


def interp_grid_2d(data, grid_x, grid_y):
    """
    interp data to shape of (grid_x, grid_y)
    :param data: dimensions of (samples, x, y)
    :param x_size:
    :param y_size:
    :return:
    """
    x, y = data.shape[-2], data.shape[-1]
    samples = np.array(range(data.shape[0]))
    def get_range(x, y):
        length = x*y*2
        return np.array(range(length//x//2, length, 2*y)), np.array(range(length//y//2, length, 2*x))

    x_range ,grid_x_range = get_range(x, grid_x)
    y_range ,grid_y_range = get_range(y, grid_y)

    interpor = RegularGridInterpolator((samples, x_range, y_range), data, bounds_error=False, fill_value=None)
    points_sample, points_x, points_y = meshgrid(samples, grid_x_range, grid_y_range)
    points = np.array(list(zip(points_sample.reshape((-1,)),
                               points_x.reshape((-1, )),
                               points_y.reshape((-1, )))))
    data_interped = interpor(points).reshape(points_sample.shape)
    return data_interped


def get_range(start, end, num):
    # get the a range of median point between start and end
    step = (end - start) / num
    return np.arange(start + step / 2, end, step)

def path_modulator(path):
    if 'linux' in sys.platform:
        return path
    else:
        path_split = path.split('/')
        return path_split[2].upper() + ':/' + '/'.join(path_split[3:])

def move_average(data, windows=10, axis=-1, allow_nan=False):
    transpose_list = list(range(len(data.shape)))
    transpose_list[axis] = -1
    transpose_list[-1] = axis
    data_transpose = data.transpose(transpose_list)
    mean_shape = data_transpose.shape[:-1]+(np.int(np.ceil(data_transpose.shape[-1]/windows)),)
    data_mean = np.empty(mean_shape)

    if allow_nan:
        mean_func = np.nanmean
    else:
        mean_func = np.mean

    for i in range(mean_shape[-1]):
        data_mean[..., i] = mean_func(data_transpose[..., i*windows:min(i*windows+windows, data_transpose.shape[-1])], axis=-1)

    data_mean_transpose = data_mean.transpose(transpose_list)
    return data_mean_transpose



if __name__ is '__main__':
    l = np.arange(11)
    _, _, a = meshgrid(l ,l, l)
    b = interp_grid_2d(a, 20 ,20)
    c = get_range(1, 2, 2)
    pass
