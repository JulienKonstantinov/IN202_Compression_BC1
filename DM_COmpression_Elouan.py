import PIL
from PIL import Image
import numpy as np
import scipy as sp
import os
from math import log10, sqrt

def load(filename):
    toLoad= Image.open(filename)
    return np.array(toLoad)

def save(array, filename):
    Image.fromarray(array).save(filename)

def psnr(original, compressed):
    mse = np.mean((original.astype(int) - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def fragment_4x4(image_array):
    assert image_array.shape[0]%4 == 0 and image_array.shape[1]%4 == 0, "L'image n'est pas divisible en blocs de 4x4"

    frag_list = []

    for i in range(0, image_array.shape[0], 4):
        frag_list.append([])
        for j in range(0, image_array.shape[1], 4):
            frag_list[-1].append(image_array[i:i+4, j:j+4, :3].copy())

    return frag_list

def defragment_4x4(array_list):
    defrag_array = np.empty([len(array_list)*4, len(array_list[0])*4, 3], dtype=np.uint8)

    for i in range(len(array_list)):
        for j in range(len(array_list[0])):
            defrag_array[i*4:i*4+4, j*4:j*4+4] = array_list[i][j]

    return defrag_array
    
if __name__ == "__main__":
    img = load("./test.png")
    
    print(psnr(img, defragment_4x4(fragment_4x4(img))))

"""
n%4 = 1, 2, 3
4 - n%4

cols_4 = cols + 4 - n%4

"""