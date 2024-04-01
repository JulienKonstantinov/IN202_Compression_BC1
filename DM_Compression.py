

import PIL
from PIL import Image
import numpy as np
import scipy as sp
import os
from math import log10, sqrt


def load(filename):
    """
    Charge une image dans un array numpy et le retourne

    Paramètres:
        filename: chemin vers l'image à charger
    """
    toLoad = Image.open(filename)
    return np.array(toLoad)


def save(array, filename):
    """
    Sauvegarde un array numpy sous la forme d'une image

    Paramètres:
        array: matrice de pixels à sauvegarder
        filename: chemin où sauvegarder la matrice
    """
    Image.fromarray(array).save(filename)


def psnr(original, compressed):
    """
    Calcul de la proximité de 2 matrices
    Fonction donnée dans l'énoncé du DM

    Paramètres:
        original: matrice originale
        compressed: matrice modifiée
    """
    mse = np.mean((original.astype(int) - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


# QUESTION 1


def padding(matrice):
    """
    Ajoute des lignes et colonnes à la matrice donnée pour qu'elle soit fragmentable en blocs de 4x4

    Paramètres:
        matrice: la matrice à modifier
    """
    reste_lignes = matrice.shape[0] % 4

    if reste_lignes != 0:
        lignes_a_ajouter = 4 - reste_lignes

    reste_colonnes = matrice.shape[1] % 4
    if reste_colonnes != 0:
        colonnes_a_ajouter = 4 - reste_colonnes

    # on crée une nouvelle matrice de la bonne taile que l'on remplit
    matrice2 = np.zeros(
        [matrice.shape[0] + lignes_a_ajouter, matrice.shape[1] + colonnes_a_ajouter, 3],
        dtype=np.uint8,
    )
    for i in range(matrice.shape[0]):
        for j in range(matrice.shape[1]):
            matrice2[i, j] = matrice[i, j]

    return matrice2


def remove_padding(matrice2, lignes, colonnes):
    """
    Retire les lignes et colonnes ajoutées à une image afin de la fragmenter
    Nécessite la taille originale de la matrice

    Paramètres:
        matrice2: matrice à modifier
        lignes, colonnes: nb lignes et colonnes de la matrice originale
    """
    matrice = np.zeros([lignes, colonnes, 3], dtype=np.uint8)
    matrice = matrice2[:lignes, :colonnes]

    return matrice


# QUESTION 2


def fragment_4x4(image_array):
    """
    Fragmente une matrice en carrés de 4x4
    Retourne une liste en 2D: [[col1.1, col1.2, col1.3], [col2.1, col2.2, col2.3]]

    Paramètres:
        image_array: matrice à fragmenter
    """
    frag_list = []

    for i in range(0, image_array.shape[0], 4):
        frag_list.append([])
        for j in range(0, image_array.shape[1], 4):
            frag_list[-1].append(image_array[i : i + 4, j : j + 4, :3].copy())

    return frag_list


def defragment_4x4(array_list):
    """
    Prends en entrée une liste 2D de la forme définie précédemment
    Retourne une matrice de taille nlignesXncols
    """
    defrag_array = np.empty(
        [len(array_list) * 4, len(array_list[0]) * 4, 3], dtype=np.uint8
    )

    for i in range(len(array_list)):
        for j in range(len(array_list[0])):
            defrag_array[i * 4 : i * 4 + 4, j * 4 : j * 4 + 4] = array_list[i][j]

    return defrag_array


# QUESTION 5

def find_color(palette, pixel):
    '''fonction qui permet de trouver la couleur d'une palette la plus proche de la couleur d'un pixel'''
    good_color=[]
    for i in range(4): #on parcourt les lignes de la palette
        somme=0
        for j in range(3): #on parcourt les colonnes de la palette
            somme+=(abs(pixel[j]-palette[i][j])) #on fait la somme des écarts en valeurs absolues entre les coordonnées RGB du pixels et d'une couleur de la palette pour toutes les couleurs de la palette
        good_color.append(somme) #on stockes toutes les sommes dans une liste
    minimum=min(good_color) 
    return palette[good_color.index(minimum)] #on retourne la couleur de la palette dont l'écart des coordonnées RGB est le plus proche du pixel

print(find_color([[4,5,6],[7,8,9],[1,2,3],[4,5,7]],[1,6,9]))

            
