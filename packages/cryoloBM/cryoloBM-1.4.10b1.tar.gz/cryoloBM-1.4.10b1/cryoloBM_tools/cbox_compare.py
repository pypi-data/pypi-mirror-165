from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import argparse
import cryolo.CoordsIO as io
from cryolo.utils import bbox_iou_vec_3d
from typing import List
from cryolo.utils import BoundBox
import numpy as np
import os


class CoordsCompare(BMTool):

    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "cbox_compare"

    def create_parser(self, parentparser: ArgumentParser) -> ArgumentParser:
        helptxt = "Comparese two cbox files. Create two now"

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
            "--first",
            required=True,
            help="First CBOX file",
        )

        req.add_argument(
            "--second",
            required=True,
            help="Second CBOX file",
        )

        req.add_argument(
            "-b",
            "--boxsize",
            type=int,
            required=True,
            help="Boxsize",
        )

        req.add_argument(
            "-t",
            "--threshold",
            type=float,
            required=True,
            help="Threshold",
        )

        req.add_argument(
            "--minsize",
            type=float,
            required=True,
            help="Minimum size",
        )

        req.add_argument(
            "--refslice",
            type=float,
            default=None,
            help="reference slice",
        )

        req.add_argument(
            "-o",
            "--out",
            required=True,
            help="Output path",
        )

    def boundbox_to_array(self, boxes: List[BoundBox], new_size=None) -> np.array:
        boxes_data = np.empty(shape=(len(boxes), 6))
        for i, box in enumerate(boxes):
            boxes_data[i, 0] = box.x + box.w / 2
            boxes_data[i, 1] = box.y + box.h / 2
            boxes_data[i, 2] = box.z
            boxes_data[i, 3] = box.w
            boxes_data[i, 4] = box.h
            d = box.depth
            if np.isnan(d):
                d = box.w
                box.depth = box.w
            boxes_data[i, 5] = d


            if new_size:
                boxes_data[i, 3] = new_size
                boxes_data[i, 4] = new_size
                boxes_data[i, 5] = new_size

        return boxes_data

    def filter_boxes(self, boxes: List[BoundBox], size: float, threshold: float):
        filtered = []
        for box in boxes:

            confidence = box.c
            bsize = box.meta["est_box_size"][0]

            if np.isnan(confidence):
                confidence = 1


            if np.isnan(bsize):
                bsize = size+1


            if confidence> threshold:# and bsize > size:
                filtered.append(box)
        return filtered

    def run(self, args):
        pth_first = args.first
        pth_second = args.second
        thresh = args.threshold
        minsize = args.minsize
        pth_out = args.out
        boxsize = args.boxsize
        iou_thresh = 0.6


        first_file_boxes = io.read_cbox_boxfile(pth_first)
        second_file_boxes = io.read_cbox_boxfile(pth_second)

        print("Number of boxes in first file:", len(first_file_boxes))
        print("Number of boxes in second file:", len(second_file_boxes))
        first_file_boxes_filtered = self.filter_boxes(first_file_boxes,
                                                      size=minsize,
                                                      threshold=thresh)
        second_file_boxes_file_boxes_filtered = self.filter_boxes(second_file_boxes,
                                                                  size=minsize,
                                                                  threshold=thresh)

        print("Number of boxes in first file (filtered):", len(first_file_boxes_filtered))
        print("Number of boxes in second file (filtered):", len(second_file_boxes_file_boxes_filtered))

        frist_np = self.boundbox_to_array(first_file_boxes_filtered,
                                          new_size=boxsize)

        second_np = self.boundbox_to_array(second_file_boxes_file_boxes_filtered,
                                           new_size=boxsize)

        in_second_matched= []
        only_first = []
        both = []
        from tqdm import tqdm

        for index_first in tqdm(range(len(frist_np))):
            box_first = frist_np[index_first,:]
            boxes_i_rep = np.array([box_first] * len(second_np))
            ious = bbox_iou_vec_3d(boxes_i_rep, second_np)
            mask = ious >= iou_thresh
            found_matches = np.where(mask)
            np.any(mask)
            if np.any(mask) == False:
                only_first.append(index_first)
            else:
                both.append(index_first)
            for i in found_matches[0]:
                #print("add", i)
                in_second_matched.append(int(i))

        in_second_matched = set(in_second_matched)
        print("in sec", len(in_second_matched),len(second_np))
        only_second = [i for i in range(len(second_np)) if int(i) not in in_second_matched]

        print("both", len(both))
        both = set(both)
        print("both", len(both))

        #print("Both", both)
        #print("First:", only_first)
        #print("Second:", only_second)


        both_boxes = [first_file_boxes_filtered[i] for i in both]
        only_first = [first_file_boxes_filtered[i] for i in only_first]
        only_second_boxes = []
        for i in only_second:
            b = second_file_boxes_file_boxes_filtered[i]
            only_second_boxes.append(b)
        only_second = only_second_boxes
        #only_second = [second_file_boxes_file_boxes_filtered[i] for i in only_second]

        os.makedirs(pth_out, exist_ok=True)

        if args.refslice:
            maxdist = (boxsize*0.2)
            both_boxes = [box for box in both_boxes if np.abs(box.z-args.refslice)<maxdist]
            only_first = [box for box in only_first if np.abs(box.z - args.refslice) < maxdist]
            only_second = [box for box in only_second if np.abs(box.z - args.refslice) < maxdist]

        io.write_cbox_file(os.path.join(pth_out, "only_second.cbox"), only_second)
        io.write_cbox_file(os.path.join(pth_out,"both.cbox"), both_boxes)
        io.write_cbox_file(os.path.join(pth_out, "only_first.cbox"), only_first)



