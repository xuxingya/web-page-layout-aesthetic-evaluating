#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Saliency Map.
"""
import math
import itertools
import cv2 as cv
import numpy as np
from utils import Util


class GaussianPyramid:
    def __init__(self, src):
        self.maps = self.__make_gaussian_pyramid(src)

    def __make_gaussian_pyramid(self, src):
        # gaussian pyramid | 0 ~ 8(1/256) . not use 0 and 1.
        maps = {'intensity': [],
                'orientations': {'0': [], '45': [], '90': [], '135': []}}
        i = src
        for x in xrange(1, 9):
            i = cv.pyrDown(i)
            if x < 2:
                continue
            buf_its = np.zeros(i.shape)
            maps['intensity'].append(i)
            for (orientation, index) in zip(sorted(maps['orientations'].keys()), xrange(4)):
                maps['orientations'][orientation].append(self.__conv_gabor(buf_its, np.pi * index / 4))
        return maps

    def __get_intensity(self, b, g, r):
        return (np.float64(b) + np.float64(g) + np.float64(r)) / 3.

    def __get_colors(self, b, g, r, i, amax):
        b, g, r = map(lambda x: np.float64(x) if (x > 0.1 * amax) else 0., [b, g, r])
        nb, ng, nr = map(lambda x, y, z: max(x - (y + z) / 2., 0.), [b, g, r], [r, r, g], [g, b, b])
        ny = max(((r + g) / 2. - math.fabs(r - g) / 2. - b), 0.)

        if i != 0.0:
            return map(lambda x: x / np.float64(i), [nb, ng, nr, ny])
        else:
            return nb, ng, nr, ny

    def __conv_gabor(self, src, theta):
        kernel = cv.getGaborKernel((8, 8), 4, theta, 8, 1)
        return cv.filter2D(src, cv.CV_32F, kernel)


class FeatureMap:
    def __init__(self, srcs):
        self.maps = self.__make_feature_map(srcs)

    def __make_feature_map(self, srcs):
        # scale index for center-surround calculation | (center, surround)
        # index of 0 ~ 6 is meaned 2 ~ 8 in thesis (Ich)
        cs_index = ((0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6))
        maps = {'intensity': [],
                'orientations': {'0': [], '45': [], '90': [], '135': []}}

        for c, s in cs_index:
            maps['intensity'].append(self.__scale_diff(srcs['intensity'][c], srcs['intensity'][s]))
            for key in maps['orientations'].keys():
                maps['orientations'][key].append(self.__scale_diff(srcs['orientations'][key][c], srcs['orientations'][key][s]))
        return maps

    def __scale_diff(self, c, s):
        c_size = tuple(reversed(c.shape))
        return cv.absdiff(c, cv.resize(s, c_size, None, 0, 0, cv.INTER_NEAREST))

    def __scale_color_diff(self, (c1, s1), (c2, s2)):
        c_size = tuple(reversed(c1.shape))
        return cv.absdiff(c1 - c2, cv.resize(s2 - s1, c_size, None, 0, 0, cv.INTER_NEAREST))


class ConspicuityMap:
    def __init__(self, srcs):
        self.maps = self.__make_conspicuity_map(srcs)

    def __make_conspicuity_map(self, srcs):
        util = Util()
        intensity = self.__scale_add(map(util.normalize, srcs['intensity']))
        orientation = np.zeros(intensity.shape)
        for key in srcs['orientations'].keys():
            orientation += self.__scale_add(map(util.normalize, srcs['orientations'][key]))
        return {'intensity': intensity, 'orientation': orientation}

    def __scale_add(self, srcs):
        buf = np.zeros(srcs[0].shape)
        for x in srcs:
            buf += cv.resize(x, tuple(reversed(buf.shape)))
        return buf


class SaliencyMap:
    def __init__(self, src):
        self.gp = GaussianPyramid(src)
        self.fm = FeatureMap(self.gp.maps)
        self.cm = ConspicuityMap(self.fm.maps)
        self.map = cv.resize(self.__make_saliency_map(self.cm.maps), tuple(reversed(src.shape[0:2])))

    def __make_saliency_map(self, srcs):
        util = Util()
        srcs = map(util.normalize, [srcs[key] for key in srcs.keys()])
        return srcs[0] / 5. + srcs[1] / 5.
