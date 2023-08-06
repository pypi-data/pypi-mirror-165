import unittest
from cryoloBM_tools import scale, priors2star, coords2warp, rotatecboxcoords
from cryoloBM import boxmanager_tools
from cryolo import CoordsIO
import os
import numpy as np

class MyTestCase(unittest.TestCase):

    def test_scale_fil_seg_file(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/segmented_fila_data/segmented_filament.box")
        output_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/")
        scale.scale(input_path=input_path,
                    output_path=output_path,
                    scale_factor=0.5)

        written_file_path = os.path.join(os.path.dirname(__file__),
                                         "../resources/out/segmented_filament.box")
        input_filaments = CoordsIO.read_eman1_helicon(input_path)
        scaled_filaments = CoordsIO.read_eman1_helicon(written_file_path)

        for fil_index, fil in enumerate(input_filaments):
            scaled_fil = scaled_filaments[fil_index]
            for boxindex, box in enumerate(fil.boxes):
                scaled_box = scaled_fil.boxes[boxindex]

                diff = np.abs(scaled_box.x * 1/0.5 - box.x)
                same = diff <= 0.001
                self.assertTrue(same, "Not the same " + str(diff))

                diff = np.abs(scaled_box.y * 1 / 0.5 - box.y)
                same = diff <= 0.001
                self.assertTrue(same, "Not the same " + str(diff))

    def test_scale_fil_seg_folder(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/segmented_fila_data/")
        output_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/")
        scale.scale(input_path=input_path,
                    output_path=output_path,
                    scale_factor=0.5)

        written_file_path = os.path.join(os.path.dirname(__file__),
                                         "../resources/out/segmented_filament.box")
        input_filaments = CoordsIO.read_eman1_helicon(os.path.join(input_path,"segmented_filament.box"))
        scaled_filaments = CoordsIO.read_eman1_helicon(written_file_path)

        for fil_index, fil in enumerate(input_filaments):
            scaled_fil = scaled_filaments[fil_index]
            for boxindex, box in enumerate(fil.boxes):
                scaled_box = scaled_fil.boxes[boxindex]

                diff = np.abs(scaled_box.x * 1/0.5 - box.x)
                same = diff <= 0.001
                self.assertTrue(same, "Not the same " + str(diff))

                diff = np.abs(scaled_box.y * 1 / 0.5 - box.y)
                same = diff <= 0.001
                self.assertTrue(same, "Not the same " + str(diff))

    def test_scale_coords_file(self):

        input_path = os.path.join(os.path.dirname(__file__),
                            "../resources/coords_data/example.coords")
        output_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/out/")
        scale.scale(input_path=input_path,
                    output_path=output_path,
                    scale_factor=0.5)


        written_file_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/example.coords")
        input_coords = np.atleast_2d(np.genfromtxt(input_path))
        written_coords = np.atleast_2d(np.genfromtxt(written_file_path))

        scal_fact_mat = 2*written_coords-input_coords

        scal_fact_mat = np.abs(scal_fact_mat)<10**-4
        print(scal_fact_mat)
        all_true = np.all(scal_fact_mat)
        os.remove(written_file_path)
        self.assertEqual(True, all_true)

    def test_priors2star(self):

        input_path_star = os.path.join(os.path.dirname(__file__),
                            "../resources/test_priors2star_data/particles.star")

        input_path_fid1 = os.path.join(os.path.dirname(__file__),
                                       "../resources/test_priors2star_data/tomo1_bin4_fid.coords")

        input_path_fid2 = os.path.join(os.path.dirname(__file__),
                                       "../resources/test_priors2star_data/tomo2_bin4_fid.coords")

        output_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/out/particles_with_prior.star")
        if os.path.exists(output_path):
            os.remove(output_path)
        priors2star.add_prior_to_star(input_path_star, [input_path_fid1,input_path_fid2], output_path)
        written = os.path.exists(output_path)
        if os.path.exists(output_path):
            pass #os.remove(output_path)
        self.assertEqual(True, written)

    def test_priors2star_match(self):
        tomonames = ["/a/b/c/str/abc.mrc", "/a/b/c/str/abc.mrc", "/a/b/c/str/abc.mrc", "/a/b/c/str/def.mrc","/a/b/c/str/def.mrc","/a/b/c/str/def.mrc"]

        fid_names = ["/a/b/c/coords/abc_bin4_fid.coords","/a/b/c/coords/def_bin4_fid.coords"]
        fid_index_list = priors2star.match(tomonames, fid_names)
        self.assertListEqual(fid_index_list[0], [0, 1, 2], "First list is different")
        self.assertListEqual(fid_index_list[1], [3, 4, 5], "Second list is different")

    def test_priors2star_match_with_star(self):
        from pyStarDB import sp_pystardb as star
        in_star = os.path.join(os.path.dirname(__file__),
                                      "../resources/test_priors2star_data/particles.star")
        sfile = star.StarFile(in_star)
        relion_dataframe = sfile['']

        tomonames = relion_dataframe['_rlnMicrographName']

        fid_names = ["/a/b/c/coords/tomo1_bin4_fid.coords","/a/b/c/coords/tomo2_bin4_fid.coords"]
        fid_index_list = priors2star.match(tomonames, fid_names)
        self.assertEqual(len(fid_index_list[0]), 1505, "First list is different")
        self.assertEqual(len(fid_index_list[1]), 1505, "Second list is different")


    def test_coords2warp(self):
        input_path_fid = os.path.join(os.path.dirname(__file__),
                                      "../resources/test_coords2warp_data/")

        output_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/")
        if os.path.exists(os.path.join(output_path,"particles_warp.star")):
            os.remove(os.path.join(output_path,"particles_warp.star"))

        pd = coords2warp.convert(
            input_path = input_path_fid,
            pixelsize = 1.75,
            magnification = 100000,
            scale = 1
        )
        self.assertEqual(True,pd != None)

    def boxes_to_array(self, boxes):
        arr = np.zeros(shape=(len(boxes),3))
        for box_i, box in enumerate(boxes):
            arr[box_i,0] = box.x
            arr[box_i,1] = box.y
            arr[box_i,2] = box.z
        return arr

    def flatten_list(self, list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]

    def test_scale_cbox_file(self):

        input_path = os.path.join(os.path.dirname(__file__),
                            "../resources/cbox_data/example3D_filament.cbox")
        output_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/out/")
        scale.scale(input_path=input_path,
                    output_path=output_path,
                    scale_factor=0.5)


        written_file_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/example3D_filament.cbox")

        input_fil = CoordsIO.read_cbox_boxfile(input_path)
        input_fil_boxes = [fil.boxes for fil in input_fil]
        input_fil_boxes = self.flatten_list(input_fil_boxes)
        input_coords = self.boxes_to_array(input_fil_boxes)

        written_fil = CoordsIO.read_cbox_boxfile(written_file_path)
        written_fil_boxes = [fil.boxes for fil in written_fil]
        written_fil_boxes = self.flatten_list(written_fil_boxes)
        written_coords = self.boxes_to_array(written_fil_boxes)
        scal_fact_mat = 2*written_coords-input_coords

        scal_fact_mat = np.abs(scal_fact_mat)<10**-4
        all_true = np.all(scal_fact_mat)
        os.remove(written_file_path)
        self.assertEqual(True, all_true)

    def test_scale_coords_folder(self):

        input_path = os.path.join(os.path.dirname(__file__),
                            "../resources/coords_data/")
        output_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/out/")
        scale.scale(input_path=input_path,
                    output_path=output_path,
                    scale_factor=0.5)


        written_file_path = os.path.join(os.path.dirname(__file__),
                                   "../resources/out/example.coords")
        input_coords = np.atleast_2d(np.genfromtxt(os.path.join(input_path,"example.coords")))
        written_coords = np.atleast_2d(np.genfromtxt(written_file_path))

        scal_fact_mat = 2*written_coords-input_coords

        scal_fact_mat = np.abs(scal_fact_mat)<10**-4
        all_true = np.all(scal_fact_mat)
        os.remove(written_file_path)
        self.assertEqual(True, all_true)

    def test_rotate_in_volume(self):

        coords = np.array([
            [0,0,0],
            [10,0,0],
            [0,10,0],
            [0,0,10],
            [1,1,1]
        ])
        exp_result = np.array([
            [0,0,0],
            [1,1,1]
        ])
        shape = np.array([5,5,5])
        res = rotatecboxcoords.RotateCBOXCoords.remove_out_of_volume_coords(coords,shape)
        np.testing.assert_array_equal(exp_result, res)

    def test_file_type_coords(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/coords_data/example.coords")
        filetype = boxmanager_tools.get_file_type(input_path)
        self.assertEqual(filetype,boxmanager_tools.TYPE_COORDS)

    def test_file_type_helicon(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/segmented_fila_data/segmented_filament.box")
        filetype = boxmanager_tools.get_file_type(input_path)
        self.assertEqual(filetype,boxmanager_tools.TYPE_EMAN_HELICON)

    def test_file_type_cbox(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/cbox_data/example3D_filament.cbox")
        filetype = boxmanager_tools.get_file_type(input_path)
        self.assertEqual(filetype,boxmanager_tools.TYPE_CBOX)


if __name__ == '__main__':
    unittest.main()
