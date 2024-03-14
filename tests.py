from DM_Compression import fragment_4x4, defragment_4x4, load, psnr, remplissage, reset_remplissage
import numpy as np


def ok(msg):
    print(f"\u001b[32m[OK]\u001b[0m {msg}")
def fail(msg):
    print(f"\u001b[31m[FAIL]\u001b[0m {msg}")

def test_fragmentation():
    test_img = load("./test.png")
    total = 0

    try:
        test_frag = fragment_4x4(test_img)
    except Exception as e:
        fail(f"Failed to fragment image: {e}")
        total += 1

    try:
        test_defrag = defragment_4x4(test_frag)
    except Exception as e:
        fail(f"Failed to defragment image: {e}")
        total += 1
    
    try:
        test_psnr = psnr(test_img, test_defrag)
    except Exception as e:
        fail(f"Failed to compute PSNR for frag: {e}")
        total += 1
    else:
        if test_psnr != 100:
            fail("Images are different for fragmentation ! PSNR != 100")
            total += 1
    
    if total == 0:
        ok("Fragmentation works fine")

def test_padding():
    test_mat = np.zeros([15, 21, 3], dtype=np.uint8)
    total = 0

    try:
        mat_pad = remplissage(test_mat)
    except Exception as e:
        fail(f"Failed to add padding: {e}")
        total += 1
    
    try:
        mat_unpad = reset_remplissage(mat_pad, 15, 21)
    except Exception as e:
        fail(f"Failed to remove padding: {e}")
        total += 1

    try:
        test_psnr = psnr(test_mat, mat_unpad)
    except Exception as e:
        fail(f"Failed to compute PSNR for padding: {e}")
        total += 1
    else:
        if test_psnr != 100:
            fail("Arrays are different for padding ! PSNR != 100")
            total += 1
    
    if total == 0:
        ok("Padding works fine")



if __name__ == "__main__":
    test_fragmentation()
    test_padding()