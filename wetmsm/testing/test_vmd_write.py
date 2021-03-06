"""Test writing data files for visualization of solvent

Author: Matthew Harrigan
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *
from unittest import TestCase
import unittest

from wetmsm import ApplyComponents
import numpy as np
from numpy.testing import assert_array_equal


class TestVmdWrite(TestCase):
    def setUp(self):
        # (frame, solvent, solute, shell)
        vent_a = 0
        vent_b = 1
        ute_1 = 0
        ute_2 = 1
        self.assn = np.array([
            [0, vent_a, ute_1, 0],
            [0, vent_b, ute_2, 0],
            [1, vent_a, ute_1, 1],
            [1, vent_b, ute_1, 1],
            [1, vent_a, ute_2, 1],
            [1, vent_b, ute_2, 1],
            [2, vent_a, ute_2, 0],
            [2, vent_b, ute_1, 0],
        ])
        # O.   'O
        # O  :  O
        # O'   .O

        self.solv = np.array([2, 3])
        self.solu = np.array([0, 1])

        class DummyTraj(object):
            n_frames = 3
            n_atoms = 5

        self.traj = DummyTraj()


    def test_add(self):
        loading2d = np.array([
            [2.0, 4.0, 99],
            [6.0, 8.0, 99]
        ])
        vmd = ApplyComponents(loading2d, self.solv, self.solu)
        user = vmd.partial_transform((self.traj, self.assn))
        sb = np.zeros((3, 5))

        sb[:, 2:4] = np.array([
            [2, 6],
            [12, 12],
            [6, 2.0]
        ])

        assert_array_equal(user, sb)

    def test_max(self):
        loading2d = np.array([
            [2.0, 4.0, 99],
            [6.0, 8.0, 99]
        ])
        vmd = ApplyComponents(loading2d, self.solv, self.solu, agg_method='max')
        user = vmd.partial_transform((self.traj, self.assn))
        sb = np.zeros((3, 5))

        sb[:, 2:4] = np.array([
            [2, 6],
            [8, 8],
            [6, 2.0]
        ])

        assert_array_equal(user, sb)

    def test_avg(self):
        loading2d = np.array([
            [2.0, 4.0, 99],
            [6.0, 9.0, 99]
        ])
        vmd = ApplyComponents(loading2d, self.solv, self.solu, agg_method='avg')
        user = vmd.partial_transform((self.traj, self.assn))
        sb = np.zeros((3, 5))

        sb[:, 2:4] = np.array([
            [2, 6],
            [6.5, 6.5],
            [6, 2.0]
        ])

        assert_array_equal(user, sb)

    def test_avg2(self):
        loading2d = np.array([
            [1.0, 0, 0],
            [1.0, 0, 0]
        ])
        vmd = ApplyComponents(loading2d, self.solv, self.solu, agg_method='avg')
        user = vmd.partial_transform((self.traj, self.assn))
        sb = np.zeros((3, 5))

        sb[:, 2:4] = np.array([
            [1, 1],
            [0, 0],
            [1, 1.0]
        ])

        assert_array_equal(user, sb)


if __name__ == "__main__":
    unittest.main()
