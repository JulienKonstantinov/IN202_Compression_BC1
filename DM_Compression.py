import PIL
from PIL import Image
import numpy as np
import scipy as sp
import os
from math import log10, sqrt

def load(filename):
    toLoad= Image.open(filename)
    return np.array(toLoad)


def psnr(original, compressed):
    mse = np.mean((original.astype(int) - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

# QUESTION 1

def remplissage(matrice):
    '''fonction qui permet de remplir une matrice de lignes et de colonnes jusqu'à ce que ses dimensions soient des multiples de 4'''

    reste1=matrice.shape[0]%4
    if reste1!=0:
        lignes_a_ajouter=4-reste1
    
    reste2=matrice.shape[1]%4
    if reste2!=0:
        colonnes_a_ajouter=4-reste2

    matrice2=np.zeros([matrice.shape[0]+lignes_a_ajouter,matrice.shape[1]+colonnes_a_ajouter,3],dtype=np.uint8)
    for i in range(matrice.shape[0]):
        for j in range(matrice.shape[1]):
            matrice2[i,j]=matrice[i,j]

    return matrice2


def reset_remplissage(matrice2,lignes, colonnes):
    '''fonction pour annuler le remplissage de la matrice et revenir à la matrice originale'''

    matrice=np.zeros([lignes,colonnes,3],dtype=np.uint8)
    matrice=matrice2[:lignes,:colonnes]

    return matrice

# QUESTION 2

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
    