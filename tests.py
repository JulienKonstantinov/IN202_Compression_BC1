import unittest
import numpy as np
from DM_Compression import padding, remove_padding, fragment_4x4, defragment_4x4, tronque, get_palette, find_color, patch_signature

class TestBC1Functions(unittest.TestCase):
    def setUp(self):
        # Create sample image array for testing
        self.image_array = np.random.randint(0, 255, size=(16, 16, 3), dtype=np.uint8)

    def test_padding(self):
        padded_array = padding(self.image_array)
        self.assertTrue(padded_array.shape[0] % 4 == 0 and padded_array.shape[1] % 4 == 0,
                        "Padding did not result in dimensions multiple of 4")

    def test_remove_padding(self):
        padded_array = padding(self.image_array)
        original_shape = self.image_array.shape
        unpadded_array = remove_padding(padded_array, original_shape[0], original_shape[1])
        self.assertTrue(np.array_equal(unpadded_array, self.image_array),
                        "Unpadding did not result in the original array")

    def test_fragment_4x4(self):
        fragmented_list = fragment_4x4(self.image_array)
        self.assertEqual(len(fragmented_list), self.image_array.shape[0] // 4,
                         "Incorrect number of rows in fragmented list")
        self.assertEqual(len(fragmented_list[0]), self.image_array.shape[1] // 4,
                         "Incorrect number of columns in fragmented list")

    def test_defragment_4x4(self):
        fragmented_list = fragment_4x4(self.image_array)
        defragmented_array = defragment_4x4(fragmented_list)
        self.assertTrue(np.array_equal(defragmented_array, self.image_array),
                        "Defragmented array is not equal to original array")

    def test_tronque(self):
        result = bin(tronque(15, 2))
        self.assertEqual(result, "0b11", "Truncation not as expected")

    def test_get_palette(self):
        palette = get_palette(np.array([0, 0, 0], dtype=np.uint8), np.array([211, 211, 211], dtype=np.uint8))
        self.assertEqual(palette.shape, (4, 3), "Palette has incorrect shape")

    def test_find_color(self):
        a, b = np.array([0, 0, 0], dtype=np.uint8), np.array([211, 211, 211], dtype=np.uint8)
        palette = get_palette(a, b)
        
        pixel = np.array([80, 108, 70], dtype=np.uint8)
        color = find_color(palette, pixel)

        self.assertEqual(color, 1, "Incorrect color index found")
    
    def test_sig_size(self):
        fragmented_list = fragment_4x4(self.image_array)

        sig = patch_signature(fragmented_list[0][0], np.array([0, 0, 0], dtype=np.uint8), np.array([211, 211, 211], dtype=np.uint8))

        self.assertEqual(len(bin(sig))-2, 64, "Signature has wrong size")

if __name__ == "__main__":
    unittest.main()
