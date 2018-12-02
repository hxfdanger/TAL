import numpy as np
import sys


def get_coefs_word(word, file_path_vec, dim_coefs=100):
    """
    entrée:
        mot à cherché
        ficher des poids d'embedding
        dimension de vecteur ('ici dim_coefs= 100 correspond à les vecteur dans le fichier')
    """

    try:
        f = open(file_path_vec)
    except IOError:
        print("Could not open file!!")
        exit()
    coefs = np.zeros((dim_coefs))

    for line in f:
        values = line.split()
        if(word == values[0]):
            coefs = np.asarray(values[1:], dtype='float32')
            break
    f.close()
    # print("here coef:  ", coefs)
    return coefs


def charger_model(file_path_vec):
    try:
        f = open(file_path_vec)
    except IOError:
        print("Could not open file!!")
        exit()
    dict = []
    for line in f:
        dict.append(line.split())

    f.close()

    return dict


def get_coefs_word_fast(word, dict, dim_coefs=100):
    coefs = np.zeros((dim_coefs))
    for vec in dict:
        if(word == vec[0]):
            coefs = np.asarray(vec[1:], dtype='float32')
            break

    return coefs


# test
if(__name__ == "__main__"):
    vec = get_coefs_word("ras zebbi", "Data/embd.vec")
    print(vec.shape)
    dict = charger_model("Data/embd.vec")
    vec = get_coefs_word_fast("ras zebbi", dict, dim_coefs=100)
    print(vec.shape)
    print(vec)
