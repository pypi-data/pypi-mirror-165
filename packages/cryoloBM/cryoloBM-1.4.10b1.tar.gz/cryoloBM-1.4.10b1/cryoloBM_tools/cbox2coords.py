

from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import argparse
from typing import List
import numpy as np
from cryolo.utils import Filament, BoundBox
from cryolo.CoordsIO import read_cbox_boxfile
from glob import glob
import os

class CBOX2Coords(BMTool):

    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "cbox2coords"

    @staticmethod
    def generate_coords_array_filaments(data: List[Filament]):
        all_fil_coords = []
        for i, fil in enumerate(data):
            coords = CBOX2Coords.generate_coords_array(fil.boxes)
            id = np.array([i]*len(fil.boxes))
            id = id.reshape((len(id),1))
            coords_fid = np.append(coords, id, axis=1)
            all_fil_coords.append(coords_fid)
        return np.concatenate(all_fil_coords)

    @staticmethod
    def generate_coords_array(data: List[BoundBox]):
        coords_dat = np.empty(shape=(len(data), 3))
        for i, box in enumerate(data):
            coords_dat[i, 0] = box.x + box.w/2
            coords_dat[i, 1] = box.y + box.h/2
            coords_dat[i, 2] = box.z
        return coords_dat

    def create_parser(self, parentparser : ArgumentParser) -> ArgumentParser:
        '''
        :param parentparser: ArgumentPaser where the subparser for this tool needs to be added.
        :return: Argument parser that was added to the parentparser
        '''
        parser = parentparser.add_parser(
            self.get_command_name(),
            help="Converts CBOX files to .coords files.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        req = parser.add_argument_group(
            "Arguments",
            "Converts CBOX files to .coords files",
        )

        req.add_argument(
            "-i",
            "--input",
            required=True,
            help="Path to folder with CBOX files ",
        )

        req.add_argument(
            "-o",
            "--out",
            required=True,
            help="Output path",
        )

        return parser


    def run(self, args):
        input_path = args.input
        output_path = args.out
        cbox_files = glob(os.path.join(input_path,"*.cbox"))


        for cbox_file in cbox_files:
            cbox_dat = read_cbox_boxfile(cbox_file)
            is_filament = isinstance(cbox_dat[0], Filament)
            filename = os.path.splitext(os.path.basename(cbox_file))[0]

            if is_filament:
                coords_dat = CBOX2Coords.generate_coords_array_filaments(cbox_dat)
            else:
                coords_dat = CBOX2Coords.generate_coords_array(cbox_dat)

            out_coords = os.path.join(output_path, "COORDS/")
            os.makedirs(out_coords, exist_ok=True)
            out_file_pth = os.path.join(out_coords, filename + ".coords")
            np.savetxt(out_file_pth, coords_dat[:, :3], fmt='%f')

            if is_filament:
                out_coords = os.path.join(output_path, "COORDS_FID/")
                os.makedirs(out_coords, exist_ok=True)
                out_file_pth = os.path.join(out_coords, filename + ".coords")
                np.savetxt(out_file_pth, coords_dat, fmt='%f')