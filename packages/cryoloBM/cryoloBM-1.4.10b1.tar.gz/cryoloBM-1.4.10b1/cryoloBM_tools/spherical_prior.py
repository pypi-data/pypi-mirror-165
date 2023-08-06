"""
Script to add priors to particles attached to virons.

1.3.2022 - Thorsten Wagner
"""

from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import numpy
import numpy as np
from eulerangles import matrix2euler
import pandas as pd
from typing import List
import argparse
from pyStarDB import sp_pystardb as star
import os

class SphericalPrior(BMTool):

    def create_parser(self, parentparser : ArgumentParser) -> ArgumentParser:

        helptxt = "Calculate priors of particles around a spherical model. It estimates 2 out of the 3 Euler angles a priori by calculating a vector from the centre of the sphere to each picked particle on the surface of the sphere."

        parser = parentparser.add_parser(
            self.get_command_name(),
            help=helptxt,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        req = parser.add_argument_group(
            "Arguments",
            helptxt,
        )

        req.add_argument("-s", "--star", required=True, help="Star file with picks for which the priors have to be calculated.")
        req.add_argument("-c", "--center", required=True, help=".coords file with center coordaintes of the spheres (e.g. virons).")
        req.add_argument("-o", "--out", required=True, help="output directory")

        return parser

    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "sphericalprior"

    @staticmethod
    def read_coords(pth: str) -> np.array:
        return np.genfromtxt(pth)

    @staticmethod
    def rotation_matrix_from_vectors(vec1: np.array, vec2: np.array):
        """ Find the rotation matrix that aligns vec1 to vec2
        :param vec1: A 3d "source" vector
        :param vec2: A 3d "destination" vector
        :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
        """
        a, b = (vec1 / numpy.linalg.norm(vec1)).reshape(3), (vec2 / numpy.linalg.norm(vec2)).reshape(3)
        v = numpy.cross(a, b)
        if any(v):  # if not all zeros then
            c = numpy.dot(a, b)
            s = numpy.linalg.norm(v)
            kmat = numpy.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            return numpy.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

        else:
            return numpy.eye(3)

    @staticmethod
    def vec_to_euler(center: np.array, coord: np.array):
        diff = coord - center
        ref = np.array([0, 0, 1])

        rot_mat = SphericalPrior.rotation_matrix_from_vectors(diff, ref)

        eulers = matrix2euler(rot_mat,
                              axes='zxz',
                              intrinsic=True,
                              right_handed_rotation=True)
        eulers[2] = eulers[2] + 90
        return eulers

    @staticmethod
    def group_by_center(centers: np.array, picks: np.array, max_distance: float) -> List[int]:
        """
        returns list of center index. -1 for invalid picks.
        """
        groups = []
        for row in picks:

            diff = centers - row
            diff = diff * diff
            diff = np.sum(diff,axis=1)
            diff = np.sqrt(diff)
            if np.min(diff) < max_distance:
                group_index = np.argmin(diff)
                groups.append(group_index)
            else:
                groups.append(-1)

        return groups

    @staticmethod
    def fill_priors(picks: pd.DataFrame, centers: np.array, groups: List[int]):
        tilts = []
        psis = []
        for row_index, row in picks.iterrows():
            coord = row[['_rlnCoordinateX', '_rlnCoordinateY', '_rlnCoordinateZ']].to_numpy().astype(float)
            center = centers[groups[row_index], :].astype(float)
            priors = SphericalPrior.vec_to_euler(center, coord)
            tilts.append(priors[1])
            psis.append(priors[2])
        if '_rlnAngleRot' not in picks:
            picks['_rlnAngleRot'] = 0
        picks['_rlnAngleTilt'] = tilts
        picks['_rlnAnglePsi'] = psis



    def run(self, args):
        pth_star = args.star
        pth_center = args.center
        pth_out = args.out

        coords = SphericalPrior.read_coords(pth_center)
        sfile = star.StarFile(pth_star)
        picks = sfile['']
        picks_rln = picks[['_rlnCoordinateX', '_rlnCoordinateY', '_rlnCoordinateZ']].to_numpy()
        coords = coords.astype(dtype=np.float)
        picks_rln = picks_rln.astype(dtype=np.float)
        groups= SphericalPrior.group_by_center(centers=coords, picks=picks_rln, max_distance=np.inf)

        SphericalPrior.fill_priors(picks=picks, centers=coords, groups=groups)

        os.makedirs(pth_out)
        new_sfile = star.StarFile(os.path.join(pth_out,os.path.basename(pth_star)))
        new_sfile.update('', picks, loop=True)
        new_sfile.write_star_file(overwrite=True)


