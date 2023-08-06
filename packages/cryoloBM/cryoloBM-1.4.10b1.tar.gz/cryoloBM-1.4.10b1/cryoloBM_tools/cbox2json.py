import glob

from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import argparse
import cryolo.CoordsIO as io
from typing import List
from cryolo.utils import BoundBox
import numpy as np
import os


class cbox2json(BMTool):


    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "cbox2json"

    def create_parser(self, parentparser: ArgumentParser) -> ArgumentParser:
        helptxt = "Converts .cbox files to EMAN .json files."
        parser = parentparser.add_parser(
            self.get_command_name(),
            help=helptxt,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        req = parser.add_argument_group(
            "Arguments",
            helptxt,
        )

        req.add_argument(
            "-i",
            "--input",
            required=True,
            nargs="+",
            help="Path to folder with .cbox files / path to single .cbox file ",
        )

        req.add_argument(
            "-n",
            "--name",
            required=True,
            help="Label for the picks",
        )

        req.add_argument(
            "-o",
            "--out",
            required=True,
            help="Output path",
        )
    def convert_to_eman_dict(self, boxes: List[BoundBox], name: str):
        eman_dict = {"boxes_3d": []}

        for box in boxes:
            c = 1.0

            if not np.isnan(box.c):
                c = box.c
            eman_dict["boxes_3d"].append([box.x+box.w/2,box.y+box.h/2,box.z,"cryolo",c,0])

        eman_dict["class_list"] = {
            "0": {
                "boxsize": int(box.w),
                "name": name
            }
        }

        return eman_dict


    def run(self, args):
        paths = []
        for pth in args.input:
            if os.path.isdir(pth):
                paths.extend(glob.glob(os.path.join(pth,"*.cbox")))
            elif os.path.isfile(pth):
                paths.append(pth)
        os.makedirs(args.out, exist_ok=True)
        for p in paths:
            boxes = io.read_cbox_boxfile(p)
            eman_dict = self.convert_to_eman_dict(boxes, args.name)
            new_filename = os.path.join(args.out, os.path.splitext(os.path.basename(p))[0] +".json")
            import json
            with open(new_filename, 'w') as fp:
                json.dump(eman_dict, fp, indent=1)
