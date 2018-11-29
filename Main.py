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


def get_mcd():
    mcd = (
        ('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA',
                                            'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
        ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    return mcd


def set_mcd(mcd):
    mcd = mcd


def get_xy(file_conllu, file_features):
    mcd = get_mcd()
    obj_generateAlltree = ConstructAllTree(file_conllu, mcd, True)

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()
    print(all_tree)
    #
    features = Features(file_features)
    for tree in all_tree:
        # tree.print_tree()

        A = Oracle(tree, features)

        A.run()

    X_onehot = features.convert_datas_to_one_hot()
    Y = np.asarray(features.labels)
    le = preprocessing.LabelEncoder()
    print("Y_train", Y)
    le.fit(Y)
    print(le.classes_)
    nb_class = len(le.classes_)
    print(nb_class)
    Y1 = le.transform(Y)
    print(Y1)
    # use one encoder
    Y_onehot = to_categorical(Y1, nb_class)
    """print(Y_train)
    # reverse to_categorical
    Y2 = argmax(Y_train, axis=1)
    print(Y2)
    # reverse LabelEncoder
    Y3 = le.inverse_transform(Y2)
    print(Y3)"""

    return X_onehot, Y_onehot


def get_data(file_features, file_train_conllu, file_test_conllu):

    # Test de la classe Oracle et Features

    # Lecture du fichier conllu

    x_train, y_train = get_xy(file_train_conllu, file_features)
    x_test, y_test = get_xy(file_test_conllu, file_features)

    return x_train, x_test, y_train, y_test


if(__name__ == "__main__"):

    x_train, x_test, y_train, y_test = get_data(
        "f1_tbp.fm", "UD_French-GSD/fr_gsd-ud-train.conllu", "UD_French-GSD/fr_gsd-ud-test.conllu")
    # x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
    print("X_train=", x_train.shape)
    print("X_test=", x_test.shape)
    print("Y_train=", y_train.shape)
    print("Y_test=", y_test.shape)
