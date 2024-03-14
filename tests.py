from DM_COmpression_Elouan import fragment_4x4, defragment_4x4, load, psnr

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
        fail(f"Failed to compute PSNR: {e}")
        total += 1
    else:
        if test_psnr != 100:
            fail("Images are different ! PSNR != 100")
            total += 1
    
    if total == 0:
        ok("Fragementation works fine")

if __name__ == "__main__":
    test_fragmentation()