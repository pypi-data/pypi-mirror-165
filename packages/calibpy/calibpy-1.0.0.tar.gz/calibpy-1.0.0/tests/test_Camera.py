import unittest
import numpy as np
from pathlib import Path
from calibpy.Camera import Camera


class TestCameraModule(unittest.TestCase):

    def setUp(self):
        print("start Camera tests...")
        self._root = Path.cwd() / "tests" / "data"

    def test_consistency(self):
        print("test_consistency...")
        cam = Camera()
        cam.quick_init()
        self.assertEqual(cam.f_mm, 50)
        self.assertEqual(cam.sensor_size_mm, (20.25, 36))
        self.assertEqual(cam.image_size, (1080, 1920))
        self.assertTrue(np.all(cam.distortion) == 0)

        ref = np.array([[2666.6666666666666666666666666667, 0, 960],
                        [0, 2666.6666666666666666666666666667, 540],
                        [0, 0, 1]])
        np.testing.assert_almost_equal(ref, cam.intrinsics)

        ref = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        np.testing.assert_almost_equal(ref, cam.RT)

        ref = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        np.testing.assert_almost_equal(ref, cam.RTb)

    def test_serializing(self):
        print("test_serializing...")
        dump_fname = str(self._root / "test.npy")
        cam = Camera()
        cam.quick_init()
        cam.serialize(dump_fname)
        cam2 = Camera()
        cam2.load(dump_fname)
        np.testing.assert_array_almost_equal(cam.intrinsics, cam2.intrinsics)
        np.testing.assert_array_almost_equal(cam.RT, cam2.RT)
        np.testing.assert_array_almost_equal(cam.RTb, cam2.RTb)
        self.assertEqual(cam.f_mm, cam2.f_mm)
        self.assertEqual(cam.sensor_size_mm, cam2.sensor_size_mm)
        self.assertEqual(cam.image_size, cam2.image_size)

        import os
        os.remove(dump_fname)


if __name__ == '__main__':
    unittest.main()
