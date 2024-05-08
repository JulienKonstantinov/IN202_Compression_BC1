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
    else:
        lignes_a_ajouter = 0

    reste_colonnes = matrice.shape[1] % 4
    if reste_colonnes != 0:
        colonnes_a_ajouter = 4 - reste_colonnes
    else:
        colonnes_a_ajouter = 0

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
# QUESTION 4


def tronque(n: int, p: int) -> bin:
    """
    Prends un entier et en retire les p bits non significatifs

    Paramètres:
        n: entier à tronquer
        p: nb de bits à tronquer
    """
    n = n >> p
    return n


def get_palette(a, b):
    """
    Génère la palette associée à a et b
    
    Paramètres:
        a, b: np.array([3], dtype=np.uint8)
    """

    palette = np.zeros([4, 3], dtype=np.uint8)
    palette[0] = a
    palette[3] = b
    palette[1] = 2/3 * a + b/3
    palette[2] = a/3 + 2/3 * b

    return palette


# QUESTION 5

def find_color(palette, pixel):
    '''fonction qui permet de trouver la couleur d'une palette la plus proche de la couleur d'un pixel'''
    good_color=[]
    for i in range(4): #on parcourt les pixels de la palette
        good_color.append(np.linalg.norm(pixel.astype(int) - palette[i])) #on stockes toutes les distances euclidiennes dans une liste
    minimum=min(good_color) 
    return good_color.index(minimum) #on retourne l'indice de la couleur de la palette dont l'écart des coordonnées RGB est le plus proche du pixel

# QUESTION 6

def color_as_sig(color):
    sig = 0
    sig += tronque(color[2], 3)
    sig = sig << 6
    sig += tronque(color[1], 2)
    sig = sig << 5
    sig += tronque(color[0], 3)

    return sig

def patch_signature(patch, a, b):
    palette = get_palette(a, b)
    signature = 0
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            color = find_color(palette, patch[i, j])
            signature = signature << 2
            signature += color

    signature = signature << 16
    signature += color_as_sig(b)
    signature = signature << 16
    signature += color_as_sig(a)
    
    return signature