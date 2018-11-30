"""
Main classe Principale
"""
from keras.utils.np_utils import to_categorical
from sklearn import preprocessing
import numpy as np
from numpy import argmax
from ConstructAllTree import *
from Features import *
from neural_network import *

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

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()[:2]
    print(len(all_tree))
    # print(all_tree)
    #
    features = Features(file_features)
    for tree in all_tree:
        # tree.print_tree()

        A = Oracle(tree, features)

        A.run()

    X_onehot = features.convert_datas_to_one_hot()
    Y_onehot = features.convert_labels_to_one_hot()

    return X_onehot, Y_onehot


def get_data(file_features, file_train_conllu, file_test_conllu):

    # Test de la classe Oracle et Features

    # Lecture du fichier conllu

    x_train, y_train = get_xy(file_train_conllu, file_features)
    print("first file ok")
    x_test, y_test = get_xy(file_test_conllu, file_features)

    return x_train, x_test, y_train, y_test


if(__name__ == "__main__"):

    x_train, x_test, y_train, y_test = get_data(
        "f1_tbp.fm", "UD_French-GSD/fr_gsd-ud-train.conllu", "UD_French-GSD/fr_gsd-ud-test.conllu")
    # x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
    print("x_train=", x_train.shape)
    print("X_test=", x_test.shape)
    print("Y_train=", y_train.shape)
    print("Y_test=", y_test.shape)

    input_dim = x_train.shape[1]
    print("input_dim= ", input_dim)
    nb_class = y_train.shape[1]
    print("nb_class= ", nb_class)
    model1 = create_neural_network_model(nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model1.fit(x_train, y_train, epochs=1000)
    score = model1.evaluate(x_test, y_test)
    print("%s: %.2f%%" % (model1.metrics_names[1], score[1] * 100))
    print("loss %f.2" % score[0])
