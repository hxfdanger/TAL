import numpy as np


def get_coefs_word(word, file_path_vec, dim_coefs=100):
    """
    entrée:
        mot à cherché
        ficher des poids d'embedding
        dimension de vecteur ('ici dim_coefs= 100 correspond à les vecteur dans le fichier')
    """
    f = open(file_path_vec)
    for line in f:
        values = line.split()
        if(word == values[0]):
            coefs = np.asarray(values[1:], dtype='float32')
            break
        else:
            coefs = np.zeros((0, dim_coefs))

    f.close()

    return coefs


# test
vec = get_coefs_word("paris", "embd.vec")
print(vec.shape)
