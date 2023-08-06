import unittest
from cryoloBM.MySketch import MyRectangle

class MyTestCase(unittest.TestCase):
    def test_resize_10_to_20(self):
        rect = MyRectangle(
            confidence = None,
            est_size = None,
            is_tomo = False,
            xy = (10,10),
            width = 100,
            height = 10,
            angle = 0,
        )
        rect.set_height(20)
        self.assertEqual(rect.xy[0], 10)
        self.assertEqual(rect.xy[1], 5)

    def test_resize_10_to_5(self):
        rect = MyRectangle(
            confidence = None,
            est_size = None,
            is_tomo = False,
            xy = (10,10),
            width = 100,
            height = 10,
            angle = 0,
        )
        rect.set_height(5)
        self.assertEqual(rect.xy[0], 10)
        self.assertEqual(rect.xy[1], 12.5)

    def test_resize_10_to_20_90degree(self):
        rect = MyRectangle(
            confidence = None,
            est_size = None,
            is_tomo = False,
            xy = (10,10),
            width = 100,
            height = 10,
            angle = 90,
        )
        rect.set_height(20)
        self.assertAlmostEqual(rect.xy[0], 5)
        self.assertAlmostEqual(rect.xy[1], 10)

    '''
    def test_resize_10_to_20_45degree(self):
        rect = MyRectangle(
            confidence = None,
            est_size = None,
            is_tomo = False,
            xy = (10,10),
            width = 100,
            height = 10,
            angle = 45,
        )
        rect.set_height(20)
        print(rect.xy)
        self.assertAlmostEqual(rect.xy[0], 5)
        self.assertAlmostEqual(rect.xy[1], 10)
    '''


if __name__ == '__main__':
    unittest.main()
