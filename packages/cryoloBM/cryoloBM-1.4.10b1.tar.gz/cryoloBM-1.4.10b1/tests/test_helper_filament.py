import unittest
from cryoloBM.helper_filament import picked_filament
import numpy as np
class MyTestCase(unittest.TestCase):

    def test_resize_height_offset_is_normalized(self):
        fil = picked_filament(30)

        fil.begin_fil = [0, 0]
        fil.end_fil = [100, 100]

        fil.set_line_params()
        self.assertAlmostEqual(np.linalg.norm(fil.offset), 1.0)

    def test_resize_height_rect_coords_get_updated_norotate(self):
        fil = picked_filament(30)

        fil.begin_fil = [0, 0]
        fil.end_fil = [0, 100]

        fil.set_line_params()
        sketch = fil.get_rect_sketch()
        fil.height = 50
        sketch_newhieght = fil.get_rect_sketch()

        self.assertAlmostEqual(25, sketch_newhieght.get_xy()[0])

    def test_resize_height_rect_coords_get_updated_rotate90(self):
        fil = picked_filament(30)

        fil.begin_fil = [0, 0]
        fil.end_fil = [100, 0]

        fil.set_line_params()
        fil.height = 50
        sketch_newhieght = fil.get_rect_sketch()

        self.assertAlmostEqual(-25, sketch_newhieght.get_xy()[1])



if __name__ == '__main__':
    unittest.main()
