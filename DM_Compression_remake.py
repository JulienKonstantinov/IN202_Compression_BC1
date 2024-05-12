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


### QUESTION 1

def get_final_shape(matrice):
    """
    Retourne la taille finale, divisible par 4, d'une matrice

    Paramètres:
        matrice: la matrice concernée
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

    return (matrice.shape[0]+lignes_a_ajouter, matrice.shape[1]+colonnes_a_ajouter)

def padding(matrice):
    """
    Ajoute des lignes et colonnes à la matrice donnée pour qu'elle soit fragmentable en blocs de 4x4

    Paramètres:
        matrice: la matrice à modifier
    """
    lignes, colonnes = get_final_shape(matrice)

    # on crée une nouvelle matrice de la bonne taile que l'on remplit
    matrice2 = np.zeros(
        [lignes, colonnes, 3],
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


### QUESTION 2

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

### QUESTION 3

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

### QUESTION 4

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

### QUESTION 5

def find_color(palette, pixel):
    """
    Trouve la couleur la plus proche dans une palette d'un pixel
    """
    good_color=[]
    for i in range(4): #on parcourt les pixels de la palette
        good_color.append(np.linalg.norm(pixel.astype(int) - palette[i])) #on stockes toutes les distances euclidiennes dans une liste
    minimum=min(good_color) 
    return good_color.index(minimum) #on retourne l'indice de la couleur de la palette dont l'écart des coordonnées RGB est le plus proche du pixel

### QUESTION  6

def get_color_signature(color):
    """
    Retourne la signature d'une couleur, en 5:6:5
    """
    sig = ""
    for k in range(3):
        if k == 1:
            s = 2
        else:
            s = 3
        sig += bin(tronque(color[k], s))[2:].zfill(8 -s)
    return sig

def patch_signature(patch, a, b):
    """
    Retourne la signature associée à un patch et ses 2 couleurs a et b
    """
    palette = get_palette(a, b)
    signature = ""
    
    signature += get_color_signature(a)
    signature += get_color_signature(b)
    for i in range(4):
        for j in range(4):
            signature += bin(find_color(palette, patch[i, j]))[2:].zfill(2)
    signature = int(signature[::-1], 2)
    
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
    """
    Trouve a et b avec la méthode du min max
    """
    r_list=[]
    g_list=[]
    b_list=[]
    for i in range(4): #on parcourt le patch et on ajoute les valeurs rgb aux trois listes
        for j in range(4):
            r_list.append(patch[i, j, 0])
            g_list.append(patch[i, j, 1])
            b_list.append(patch[i, j, 2])
    
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
    """
    Trouve a et b avec la méthode de la dérivation standard
    """
    r_list=[]
    g_list=[]
    b_list=[]
    for i in range(len(patch)): #on parcourt le patch et on ajoute les valeurs rgb aux trois listes
        for j in range(len(patch[i])):
            r_list.append(patch[i,j][0])
            g_list.append(patch[i,j][1])
            b_list.append(patch[i,j][2])

    minus_r=np.mean(r_list)-np.std(r_list) #cas de la moyenne moins l'écart type
    minus_g=np.mean(g_list)-np.std(g_list)
    minus_b=np.mean(b_list)-np.std(b_list)
    plus_r=np.mean(r_list)+np.std(r_list) #cas de la moyenne plus l'écart type
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


### QUESTION 7 ET 8

def create_file(image, find_color_method=1, path=None):
    """
    Transforme une image, chargée dans une matrice, en un fichier BC1

    Paramètres:
        image: la matrice de l'image
        find_color_method: valeurs possibles: 1 ou 2, si 1 alors minmax, si 2 alors moyenne et dérivation standard
        path: chemin du fichier à écrire
    """
    if not path:
        ftypes = (("BC1 Images", "*.bc1"), ("All files", "*.*"))
        path=asksaveasfilename(filetypes=ftypes) #demander à l'utilisateur où il veut sauvegarder le fichier

    file = open(path,'w')
    file.write("BC1"+"\n"+str(image.shape[0])+" "+str(image.shape[1])+"\n") #écriture BC1 et dimensions de l'image

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

### QUESTION 9

def load_bc1_file(path=None):
    """
    Charge le fichier donné, retourne la liste des signatures des patch et la dimension de l'image
    """
    if not path:
        ftypes = (("BC1 Images", "*.bc1"), ("All files", "*.*"))
        path = askopenfilename(filetypes=ftypes) #demander à l'utilisateur quel fichier il souhaite ouvrir

    with open(path, "r") as f:
        lines = f.readlines()
    
    if not lines[0].startswith("BC1"): #si la première ligne ne contient pas BC1, on s'arrête
        return
    
    im_dims = [int(x) for x in lines[1].strip().split(" ")]
    sigs = []
    for line in lines[2:]:
        line = bin(int(line))[2:]
        line = (64-len(line))*"0" + line
        line = line[::-1]
        sigs.append(line)

    return sigs, im_dims

### QUESTION 10

def get_signature_color(sig):
    """
    Transforme la partie réservée à la signature d'une couleur en une couleur
    """
    r, g, b = sig[:5], sig[5:11], sig[11:]
    return np.array([int(r, 2) << 3, int(g, 2) << 2, int(b, 2) << 3], dtype=np.uint8)

def sig_to_patch(sig):
    """
    Transforme la signature d'un patch en un patch
    """
    a, b = sig[0:16], sig[16:32]
    a = get_signature_color(a)
    b = get_signature_color(b)

    palette = get_palette(a, b)
    patch = np.zeros((4, 4, 3), dtype=np.uint8)

    sig = sig[32:]
    for i in range(4):
        for j in range(4):
            
            num = sig[((i*4)+j)*2] + sig[((i*4)+j)*2 + 1]
            num = int(num, 2)
            patch[i, j] = palette[num]
    
    return patch

def uncompress(sig_list, dims):
    """
    Prends la liste des signatures et retourne l'image fragmentée 
    """
    padded_dims = get_final_shape(np.empty(dims, dtype=np.uint8))
    frag_list = []

    for j in range(len(sig_list)):
        sig_list[j] = sig_to_patch(sig_list[j])
    
    i = 0
    while not sig_list == []:
        frag_list.append([])
        for i in range(dims[1]//4):
            frag_list[-1].append(sig_list[0])
            sig_list.pop(0)

    return frag_list

