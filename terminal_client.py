from DM_Compression_remake import *
from sys import exit

im_path = ""

def print_status():
    
    if im_path:
        print(f"FILE LOADED: {im_path}")
    else:
        print(f"NO FILE LOADED")
    print("--- q: quit | l: load a file | c: compress file if possible | d: decompress file if possible ---")

print("Welcome to this BC1 compressor cli")

while True:
    print_status()
    choice = input("\t$ ")
    if choice == "q":
        print("Exiting...")
        exit()
    elif choice == "l":
        ftypes = (("All files", "*.*"), )
        im_path = askopenfilename(filetypes=ftypes)
        if im_path:
            print("PATH OK")
        else:
            print("Action aborted")
    elif choice == "c":
        ftypes = (("BC1 images", "*.bc1"), ("All files", "*.*"))
        tosave = asksaveasfilename(filetypes=ftypes)
        if tosave:
            try:
                create_file(load(im_path), path=tosave)
            except Exception as e:
                print(f"An error occured: {e}")
            else:
                print("Compression successful")
        else:
            print("Action aborted")
    elif choice == "d":
        ftypes = (("PNG images", "*.png"), ("All files", "*.*"))
        tosave = asksaveasfilename(filetypes=ftypes)
        if tosave:
            try:
                f, d = load_bc1_file(im_path)
                f = defragment_4x4(uncompress(f, d))
                f = remove_padding(f, d[0], d[1])
                save(f, tosave)
            except Exception as e:
                print(f"An error occured: {e}")
            else:
                print("Compression successful")
        else:
            print("Action aborted")