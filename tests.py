import unittest
import numpy as np
from DM_Compression_remake import *

class TestBC1Functions(unittest.TestCase):
    def setUp(self):
        # Create sample image array for testing
        self.image_array = np.random.randint(0, 255, size=(16, 16, 3), dtype=np.uint8)
        self.image_array_wrong_padding = np.random.randint(0, 255, size=(17, 15, 3), dtype=np.uint8)

    def test_padding(self):
        padded_array = padding(self.image_array_wrong_padding)
        self.assertTrue(padded_array.shape[0] % 4 == 0 and padded_array.shape[1] % 4 == 0,
                        "Padding did not result in dimensions multiple of 4")
        self.assertTrue(padded_array.shape[0] == 20 and padded_array.shape[1] == 16,
                        "Padding is wrong !")

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
    
    def test_patch_signature(self):
        a = np.array([0, 0, 0], dtype=np.uint8)
        b = np.array([255, 255, 255], dtype=np.uint8)
        patch = np.random.randint(0, 255, size=(4, 4, 3), dtype=np.uint8)
        signature = patch_signature(patch, a, b)
        self.assertIsInstance(signature, int, "Signature is not integer type")

    def test_create_file(self):
        create_file(self.image_array, find_color_method=1, path="test_file.bc1")
        self.assertTrue(os.path.exists("test_file.bc1"), "BC1 file not created")

    def test_load_bc1_file(self):
        sigs, im_dims = load_bc1_file("test_file.bc1")
        self.assertIsInstance(sigs, list, "Signatures not loaded as list")
        self.assertIsInstance(im_dims, list, "Image dimensions not loaded as list")
    
    def test_get_signature_color(self):
        sig = "01010101010000000001111111111111"
        color = get_signature_color(sig)
        self.assertTrue(np.array_equal(color, np.array([5, 10, 31], dtype=np.uint8)),
                        "Signature color not as expected")

    def test_sig_to_patch(self):
        sig = "000000000000000001111111111111110000000000000000111111111111111100000000000000001111111111111111"
        patch = sig_to_patch(sig)
        self.assertEqual(patch.shape, (4, 4, 3), "Patch shape not as expected")

    def test_uncompress(self):
        sig_list = ["000000000000000001111111111111110000000000000000111111111111111100000000000000001111111111111111"] * 16
        dims = (16, 16, 3)
        frag_list = uncompress(sig_list, dims)
        self.assertEqual(len(frag_list), 4, "Uncompressed list rows not as expected")
        self.assertEqual(len(frag_list[0]), 4, "Uncompressed list columns not as expected")

if __name__ == "__main__":
    unittest.main()
