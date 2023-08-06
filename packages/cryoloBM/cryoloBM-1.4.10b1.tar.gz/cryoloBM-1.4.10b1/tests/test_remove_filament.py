import unittest
from cryoloBM.helper_filament import picked_filament
from cryoloBM.helper_image import is_click_into_box

def create_fil(boxsize,begin,end):
    fil = picked_filament(box_size=boxsize)
    fil.begin_fil = begin
    fil.end_fil = end
    fil.set_line_params()
    return fil.get_rect_sketch()


class vertical_down_up(unittest.TestCase):
    # vertical filament picked from down to up
    boxsize = 200
    fil = create_fil(boxsize=boxsize,begin=[771.5451467268621, 457.17945823927755],end= [790.0372460496613, 3378.9311512415347])

    def test_clicked_out(self):
        self.assertFalse( is_click_into_box(fil=self.fil,x=1206,y=1853,boxsize=self.boxsize,is_tomo=False))

    def test_clicked_in(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=762, y=1492, boxsize=self.boxsize, is_tomo=False))

class vertical_up_down(unittest.TestCase):
    # vertical filament picked from up to down
    boxsize = 200
    fil = create_fil(boxsize=boxsize,begin=[2112.2223476297963, 3351.193002257336],end= [2065.992099322799, 762.2990970654627])

    def test_clicked_out(self):
        self.assertFalse( is_click_into_box(fil=self.fil,x=2620,y=2139,boxsize=self.boxsize,is_tomo=False))

    def test_clicked_in(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=2093, y=2093, boxsize=self.boxsize, is_tomo=False))


class horizontal_left_right(unittest.TestCase):
    # horizontal filament picked left to right
    boxsize = 200
    fil = create_fil(boxsize=boxsize, begin=[429.44130925507886, 3064.5654627539498],
                     end=[3147.779909706546, 3036.827313769751])

    def test_clicked_out_up(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=2056, y=3746, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_down(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=1853, y=2685, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_right(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=3480, y=3064, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_left(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=179, y=3120, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_center(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=1779, y=3073, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_left(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=854, y=3046, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_right(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=2851, y=3009, boxsize=self.boxsize, is_tomo=False))

class horizontal_right_left(unittest.TestCase):
    # horizontal filament picked right to left
    boxsize = 200
    fil = create_fil(boxsize=boxsize, begin=[2953.6128668171555, 725.3148984198644],
                     end=[484.91760722347624, 734.560948081264])

    def test_clicked_out_up(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=1733, y=1095, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_down(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=1760, y=336, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_right(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=3499, y=706, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_left(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=198, y=753, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_center(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=1760, y=734, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_left(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=743, y=716, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_right(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=2546, y=716, boxsize=self.boxsize, is_tomo=False))


class diagonal_left_up_right_down(unittest.TestCase):
    # horizontal filament from left up to right down right
    boxsize = 200
    fil = create_fil(boxsize=boxsize, begin=[3536.1139954853265, 3582.3442437923245],
                     end= [762.2990970654627, 1002.6963882618508])

    def test_clicked_out_up(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=1751, y=2824, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_down(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=2454, y=1927, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_right(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=3582, y=3702, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_left(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=679, y=910, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_center(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=2065, y=2213, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_left(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=2384, y=2421, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_right(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=3027, y=3110, boxsize=self.boxsize, is_tomo=False))



class diagonal_right_up_left_down(unittest.TestCase):
    # horizontal filament from right up to left down right
    boxsize = 200
    fil = create_fil(boxsize=boxsize, begin=[336.9808126410834, 3221.748306997742],
                     end=[3240.2404063205418, 836.267494356659])

    def test_clicked_out_up(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=2121, y=2250, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_down(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=1169, y=1686, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_right(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=3508, y=669, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_out_left(self):
        self.assertFalse(is_click_into_box(fil=self.fil, x=124, y=3378, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_center(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=1705, y=2180, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_left(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=438, y=3083, boxsize=self.boxsize, is_tomo=False))

    def test_clicked_in_right(self):
        self.assertTrue(is_click_into_box(fil=self.fil, x=3046, y=1021, boxsize=self.boxsize, is_tomo=False))


if __name__ == '__main__':
    unittest.main()
