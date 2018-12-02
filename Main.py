"""
Main classe Principale
"""

from keras.utils.np_utils import to_categorical
from sklearn import preprocessing
import numpy as np
from numpy import argmax
from ConstructAllTree import *
from Features import *
from Oracle import *

from neural_network import create_neural_network_model


def get_mcd():
    mcd = (
        ('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA',
                                            'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
        ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    return mcd


def set_mcd(mcd):
    mcd = mcd


def get_xy(file_conllu, file_features, file_embedding=None):
    mcd = get_mcd()

    print("Chargement des arbres")
    obj_generateAlltree = ConstructAllTree(file_conllu, mcd, True)

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()
    # print(all_tree[0].print_tree())
    print("Arbres charger : ", len(all_tree))

    print("Création du dataset")
    features = Features(file_features)
    i = 0
    for tree in all_tree:
        i += 1
        if i % 1000 == 0:
            print(i)
        # tree.print_tree()
        # if i != 43 and i != 61:
        A = Oracle(tree, features)
        A.run()

    print("Convertion du dataset")
    print("file_embedding : ", file_embedding)
    X, Y = features.get_Data_Set(file_embedding)
    """X_onehot = features.convert_datas_to_one_hot()

	Y_onehot = features.convert_labels_to_one_hot()"""
    return X, Y


def get_data(file_features, file_train_conllu, file_embedding=None):

    x_train, y_train = get_xy(file_train_conllu, file_features, file_embedding)

    return x_train, y_train


if(__name__ == "__main__"):

    features_file = "Data/f1_tbp.fm"
    #conllu_file = "Data/fr_gsd-ud-train.conllu"
    conllu_file = "UD_French-GSD/fr_gsd-ud-train.conllu"
    weight_embedding_file = "Data/embd_fr_50.vec"
    x_train, y_train = get_data(
        features_file, conllu_file)
    # x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
    print("x_train=", x_train.shape)
    print("Y_train=", y_train.shape)
    print("save file")
    """outfile_X = "X_f3_JAP.npy"
    outfile_Y = "Y_f3_JAP.npy"
    np.save(outfile_X, x_train)
    np.save(outfile_Y, y_train)"""
