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
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

#Question1

mat_test=np.zeros([15,21,3],dtype=np.uint8)

def remplissage(matrice):
    '''fonction qui permet de remplir une matrice de lignes et de colonnes jusqu'à ce que ses dimensions soient des multiples de 4'''

    reste1=mat_test.shape[0]%4
    if reste1!=0:
        lignes_a_ajouter=4-reste1
    
    reste2=mat_test.shape[1]%4
    if reste2!=0:
        colonnes_a_ajouter=4-reste2

    matrice2=np.zeros([matrice.shape[0]+lignes_a_ajouter,matrice.shape[1]+colonnes_a_ajouter,3],dtype=np.uint8)
    for i in range(matrice.shape[0]):
        for j in range(matrice.shape[1]):
            matrice2[i,j]=matrice[i,j]

    return matrice2

print(remplissage(mat_test).shape)

def reset_remplissage(matrice2,lignes,colonnes):
    '''fonction pour annuler le remplissage de la matrice et revenir à la matrice originale'''

    matrice=np.zeros([lignes,colonnes,3],dtype=np.uint8)
    matrice=matrice2[:lignes,:colonnes]

    return matrice

print(reset_remplissage(mat_test,15,21).shape)
