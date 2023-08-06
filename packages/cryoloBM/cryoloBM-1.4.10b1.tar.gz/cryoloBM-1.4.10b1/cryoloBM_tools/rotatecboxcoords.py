from argparse import ArgumentParser
import argparse
from cryoloBM.bmtool import BMTool
from cryolo.utils import Filament, BoundBox
from cryolo.CoordsIO import read_cbox_boxfile, write_cbox_file
from dataclasses import dataclass
from typing import Tuple, List, Dict
import numpy as np
import os
import glob
import tqdm

@dataclass
class RotationMeta:
    filename_unrotated : str
    filename_rotated : str
    rotation : Tuple[float, float, float] # x,y,z
    dimension_orig : Tuple[int, int, int] # x,y,z
    dimension_rotated : Tuple[int, int, int] # x,y,z


class RotateCBOXCoords(BMTool):



    def run(self, args):
        cbox_path = args.input
        meta_path = args.meta
        output_path= args.out
        zfloat = args.zfloat
        extr_boxsize = args.boxsize

        cbox_files = self.get_cbox_files_paths(cbox_path)
        rotation_data = self.get_rotation_data(meta_path)
        matched_pairs = self.match_cbox_rotation_data(cbox_files=cbox_files, rotation_meta=rotation_data)
        for cbox_path, rotation_meta in tqdm.tqdm(matched_pairs, desc="Rotate"):
            cbox_dat = read_cbox_boxfile(cbox_path)
            is_filament = isinstance(cbox_dat[0], Filament)
            if is_filament:
                # filament path
                rotated_dat= self.rotate_filaments(filaments=cbox_dat, meta=rotation_meta,extraction_box_size=extr_boxsize)



            else:
                # bounding box path
                rotated_dat = self.rotate_boundingbox(boxes=cbox_dat, meta_path=rotation_meta, extraction_box_size=extr_boxsize)
                if not zfloat:
                    for box in rotated_dat:
                        box.z = int(round(box.z))

            filename = os.path.splitext(os.path.basename(rotation_meta.filename_unrotated))[0]

            out_cbox = os.path.join(output_path,"CBOX/")
            os.makedirs(out_cbox, exist_ok=True)
            out_file_pth = os.path.join(out_cbox, filename+".cbox")
            write_cbox_file(path=out_file_pth, coordinates=rotated_dat)


    @staticmethod
    def match_cbox_rotation_data(cbox_files: List[str], rotation_meta: List[RotationMeta]):
        pairs=[]
        for meta in rotation_meta:
            for pth in cbox_files:
                filename = os.path.splitext(os.path.basename(pth))[0]
                if filename in meta.filename_rotated:
                    pairs.append((pth,meta))
        return pairs

    @staticmethod
    def remove_out_of_volume_coords(coords: np.array, vol_dim : np.array, box_size = 0) -> np.array:
        mask = np.array([True]*coords.shape[0])
        for i in range(len(vol_dim)):
            mask_dim = np.logical_and(coords[:,i]>=box_size,coords[:,i] < (vol_dim[i] - box_size/2))
            mask = np.logical_and(mask,mask_dim)
        return coords[mask]

    def create_parser(self, parentparser: argparse.ArgumentParser) -> ArgumentParser:
        parser_cbox_rotate = parentparser.add_parser(
            self.get_command_name(),
            help="Given coordinates of from a rotated tomogram it rotates them back to a unrotated tomogram.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        req = parser_cbox_rotate.add_argument_group(
            "Arguments",
            "Add filament prior information to star",
        )

        req.add_argument(
            "-i",
            "--input",
            required=True,
            help="Path to folder with CBOX files that are to rotate ",
        )

        req.add_argument(
            "-m",
            "--meta",
            required=True,
            help="Path to meta file",
        )

        req.add_argument(
            "-o",
            "--out",
            required=True,
            help="Path to output dir.",
        )

        req.add_argument(
            "--zfloat",
            default=False,
            action="store_true",
            help="If set, z is NOT converted to an integer"
        )

        req.add_argument(
            "--boxsize",
            default=-1,
            type=int,
            help="Extraction box size that should be taken into account when checking if rotated boxes are within the volume. If not provided, box size of CBOX files is used"
        )

        return parser_cbox_rotate


    def get_command_name(self) -> str:
        return "rotate"

    @staticmethod
    def get_rotation_data(meta: str) -> List[RotationMeta]:
        import pandas as pd
        dat = pd.read_csv(meta, header=None)
        meta_data=[]
        for _, row in dat.iterrows():
            meta = RotationMeta(
                filename_unrotated=row[0],
                filename_rotated=row[1],
                rotation=(float(np.radians(row[2])),
                          float(np.radians(row[3])),
                          float(np.radians(row[4]))),
                dimension_orig=(row[5],row[6],row[7]),
                dimension_rotated=(row[8],row[9],row[10]),
            )
            meta_data.append(meta)
        return meta_data

    @staticmethod
    def get_cbox_files_paths(pth: str):
        files = glob.glob(os.path.join(pth,"*.cbox"))
        return files

    def rotate_boundingbox(self, boxes : List[BoundBox], meta : RotationMeta, extraction_box_size = -1) -> List[BoundBox]:
        '''
        Rotates the bounding boxes according rotation meta
        '''

        # create numpy array with x,y,z, apply necessary conversions
        coords = np.zeros(shape=(len(boxes),3))
        avg_box_size = 0
        for i, b in enumerate(boxes):
            coords[i,0] = b.x + b.w/2
            coords[i,1] = b.y + b.h/2
            coords[i,2] = b.z
            avg_box_size += b.w
        avg_box_size = avg_box_size/len(boxes)
        if extraction_box_size != -1:
            avg_box_size = extraction_box_size



        rotated_boxes = []

        points = self.rotate_points(coords_raw=coords, meta=meta)

        points = RotateCBOXCoords.remove_out_of_volume_coords(points, meta.dimension_rotated, box_size=avg_box_size)


        for row_index, row in enumerate(points):
            box = BoundBox(x=row[0]-boxes[row_index].w/2,
                           y=row[1]-boxes[row_index].h/2,
                           z=row[2],
                           w=boxes[row_index].w,
                           h=boxes[row_index].h,
                           c=boxes[row_index].c,
                           depth=1)
            rotated_boxes.append(box)

        return rotated_boxes

    def rotate_filaments(self, filaments : List[Filament],
                         meta : RotationMeta,
                         extraction_box_size : int = 0
                         ) -> List[Filament]:
        '''
        Rotates the filament positions.
        '''

        rotated_filaments: List[Filament] = []

        for filament in filaments:
            boxes = filament.boxes
            rotated_boxes = [self.rotate_boundingbox(boxes=boxes,meta=meta,extraction_box_size=extraction_box_size)]
            for boxes in rotated_boxes:
                f = Filament(boxes=boxes)
                rotated_filaments.append(f)

        return rotated_filaments


    def rotate_points(self, coords_raw, meta : RotationMeta):

        # calc from meta
        thickness_rot = meta.dimension_rotated[2]
        thickness_ori= meta.dimension_orig[2]
        rot_angles_xyz = meta.rotation
        tomogram_dimensions_original = (meta.dimension_orig[0],meta.dimension_orig[1])
        # Translation to shift the origin to the center
        '''
        coords_columnsplit = np.hsplit(coords_raw, 4)
        coords = np.column_stack(
            (coords_columnsplit[0], coords_columnsplit[1], coords_columnsplit[2])
        )
        '''
        #print(coords_raw)
        coords = coords_raw
        recoords_matrix = np.array([-meta.dimension_rotated[0] / 2, -meta.dimension_rotated[1] / 2,
                                    -float(thickness_rot / 2)])
        coords_shifted = np.add(coords, recoords_matrix)

        # Invert coords array for rotation
        coords_inv = coords_shifted.swapaxes(0, 1)

        # Calculate rotation matrix
        rotx, roty, rotz = rot_angles_xyz
        R_z = np.array(
            [[np.cos(rotz), -np.sin(rotz), 0], [np.sin(rotz), np.cos(rotz), 0], [0, 0, 1]]
        )
        R_y = np.array(
            [[np.cos(roty), 0, np.sin(roty)], [0, 1, 0], [-np.sin(roty), 0, np.cos(roty)]]
        )
        R_x = np.array(
            [[1, 0, 0], [0, np.cos(rotx), -np.sin(rotx)], [0, np.sin(rotx), np.cos(rotx)]]
        )
        R = np.dot(R_x, np.dot(R_y, R_z))
        R_inv = np.linalg.inv(R)

        # Rotate the points
        new_coords_inv = np.dot(R_inv, coords_inv)

        # Revert coords and shift back the origin to the corner
        new_coords = new_coords_inv.swapaxes(0, 1)

        recoords_matrix_inv = np.array(
            [tomogram_dimensions_original[0] / 2, tomogram_dimensions_original[1] / 2,
             float(thickness_ori / 2)]
        )  # Half dimension orignal tomogram
        new_coords_recoords = np.add(new_coords, recoords_matrix_inv)
       # final = np.column_stack((new_coords_recoords))


        return new_coords_recoords