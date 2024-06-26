import PIL
from PIL import Image
import numpy as np
import scipy as sp
import os
from math import log10, sqrt
from tkinter.filedialog import askopenfilename,asksaveasfilename


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
            matrice2[i, j] = matrice[i, j, :3]

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
    if p>0:
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


def get_all_indices(patch, a, b):
    palette = get_palette(a, b)
    indices = []
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            indices.append(bin(find_color(palette, patch[i, j]))[2:])
    return indices 

def get_color_signature(color):
    signature = ""

    signature += bin(tronque(color[2], 3))[2:]
    signature += bin(tronque(color[1], 2))[2:]
    signature += bin(tronque(color[0], 3))[2:]

    return signature

def patch_signature(patch, a, b):
    signature = "".join(get_all_indices(patch, a, b))
    signature += get_color_signature(b)
    signature += get_color_signature(a)

    signature = int(signature, 2)
    return signature

# Partie 3 méthode 1
def get_color(r, g, b):
    """
    Retourne un np.array([3], dtype=np.uint8) avec les couleurs passées au moulin du 5:6:5
    """
    prepare = lambda x, z: (x >> z) << z
    r = prepare(r, 3)
    g = prepare(g, 2)
    b = prepare(b, 3)

    return np.array([r, g, b], dtype=np.uint8)


def find_a_b(patch):
    r_list=[]
    g_list=[]
    b_list=[]
    for i in range(len(patch)):
        for j in range(len(patch[i])):
            r_list.append(patch[i,j][0])
            g_list.append(patch[i,j][1])
            b_list.append(patch[i,j][2])
    
    min_r=min(r_list)
    min_g=min(g_list)
    min_b=min(b_list)
    max_r=max(r_list)
    max_g=max(g_list)
    max_b=max(b_list)

    a=get_color(min_r, min_g, min_b)
    
    b=get_color(max_r, max_g, max_b)
    
    return (a,b)


# Partie 3 méthode 2

def find_a_b_2(patch):
    r_list=[]
    g_list=[]
    b_list=[]
    for i in range(len(patch)):
        for j in range(len(patch[i])):
            r_list.append(patch[i,j][0])
            g_list.append(patch[i,j][1])
            b_list.append(patch[i,j][2])

    minus_r=np.mean(r_list)-np.std(r_list)
    minus_g=np.mean(g_list)-np.std(g_list)
    minus_b=np.mean(b_list)-np.std(b_list)
    plus_r=np.mean(r_list)+np.std(r_list)
    plus_g=np.mean(g_list)+np.std(g_list)
    plus_b=np.mean(b_list)+np.std(b_list)

    a= np.array([minus_r,minus_g,minus_b], dtype=np.uint8)
    b= np.array([plus_r,plus_g,plus_b], dtype=np.uint8)
    for k in range(3):
        if k == 1:
            a[k] = tronque(a[k], 2) << 2
            b[k] = tronque(b[k], 2) << 2
        else:
            a[k] = tronque(a[k], 3) << 3
            b[k] = tronque(b[k], 3) << 3

    return (a,b)



# QUESTION 7 et 8
def create_file(image, find_color_method = 1, path=None):
    if not path:
        ftypes = (("BC1 Images", "*.bc1"), ("All files", "*.*"))
        path=asksaveasfilename(filetypes=ftypes)

    file = open(path,'w')
    file.write("BC1"+"\n"+str(image.shape[0])+" "+str(image.shape[1])+"\n")

    dim = padding(image)
    frag_im=fragment_4x4(dim)
    for line in frag_im:
        for patch in line:
            if find_color_method == 1:
                get_ab = find_a_b
            elif find_color_method == 2:
                get_ab = find_a_b_2
            else:
                raise ValueError(f"Method {find_color_method} do not exist")
            a, b = get_ab(patch)
            file.write(str(patch_signature(patch, a, b))+"\n")
    file.close()


# QUESTION 9 et 10
        
def read_file(path=None):
    if not path:
        ftypes = (("BC1 Images", "*.bc1"), ("All files", "*.*"))
        path = askopenfilename(filetypes=ftypes)

    list_patch=[]
    file=open(path,'r')
    lines = file.readlines()
    file.close()

    if not lines[0].startswith("BC1"):
        return
    
    dims = [int(x) for x in lines[1].strip().split(" ")]

    for line in lines[2:]:
        list_patch.append(bin(int(line))[2:][::-1])

    uncompressed_im = uncompress(dims, list_patch)

    save(uncompressed_im, path.split(".")[0] + ".jpg")

def get_color_from_sig(col):
    r = col[0:5]
    g = col[5:11]
    b = col[11:16]

    r = int(r+"0"*3, 2)
    g = int(g+"0"*2, 2)
    b = int(b+"0"*3, 2)

    return np.array([r, g, b], dtype=np.uint8)

def sig_as_patch(signature):
    signature = "0" * (64 - len(signature)) + signature
    patch = np.empty((4, 4, 3), dtype=np.uint8)
    a, b = get_color_from_sig(signature[0:16]), get_color_from_sig(signature[16:32])
    palette = get_palette(a, b)
    print(palette)
    x = 32
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            patch[i, j] = palette[int(signature[x:x+2], 2)]
            x += 2
    return patch

def uncompress(dims, list_patch, path=None):
    final = []

    for i in range(dims[0]//4):
        final.append([])
        for j in range(dims[1]//4):
            
            final[-1].append(sig_as_patch(list_patch[i*4 + j]))
    
    final = defragment_4x4(final)
    return final


# create_file(load("toto.png"), path="toto.bc1")
read_file("fin.bc1")