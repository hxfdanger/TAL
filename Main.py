"""
Main classe Principale
"""

from keras.utils.np_utils import to_categorical
from keras import models
from sklearn import preprocessing
import numpy as np
from numpy import argmax
from ConstructAllTree import *
from Features import *
from Oracle import *
from Transform_Tree_Conllu import *
from keras.models import load_model
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
    # print(obj_generateAlltree.get_corpus())
    # print(obj_generateAlltree.get_vocabulary())

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()
    # print(all_tree[0].print_tree())
    print("Arbres charger : ", len(all_tree))

    print("Création du dataset")
    features = Features(file_features)
    i = 0
    for tree in all_tree:

        # tree.print_tree()
        # if i != 43 and i != 61:
        A = Oracle(tree, features)
        A.run()
    #
    # print(features.datas)
    #
    # print(features.labels_encoders)
    print("Convertion du dataset")
    print("file_embedding : ", file_embedding)
    X, Y = features.get_Data_Set(file_embedding)

    labels_encoderX = features.get_label_encoderX()
    labels_encoderY = features.get_label_encoderY()

    print("X_train_shape", X.shape)
    print("Y_train_shape", Y.shape)

    return X, Y, labels_encoderX, labels_encoderY, all_tree


def get_data(file_features, file_train_conllu, file_embedding=None):

    x_train, y_train, labels_encoderX, labels_encoderY, all_tree = get_xy(
        file_train_conllu, file_features, file_embedding)

    return x_train, y_train, labels_encoderX, labels_encoderY, all_tree


def get_model(x_train, y_train, nb_class, input_dim):
    print(x_train.shape)
    print(y_train.shape)
    print(nb_class)
    print(input_dim)
    print(y_train)
    model = create_neural_network_model(nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model.fit(x_train, y_train, epochs=50)

    y_pred = model.predict(x_train[:2])
    print(y_pred)

    model.save("test_model.h5")

    print("fin")
    return model


def main(filetrainConllu, filetestConllu, features_file, file_genarate, model_file=None):
    """
        construire le dataset
    train le model
    automate classfier , testdaset
    build file conllu from tree
    build scrip evaluation


    :param model_file: fichier h5
    :param filetestConllu: fichier conllu pour compare le resultat
    :param filetesttxt:
    :param features_file:
    :return:
    """

    print("Chargement de données ...")
    # conllu_file = "Data/fr_gsd-ud-train.conllu"
    # conllu_file = "Data/fr_gsd-ud-train.conllu"
    # weight_embedding_file = "embd_file_vectors/embd.vec"

    x_train, y_train, labels_encoderX, labels_encoderY, all_tree = get_data(
        features_file, filetrainConllu)

    # x_test, y_test,features_Xtest=get_data (features_file, filetestConllu)

    all_tree_automate = list()

    print("Train model ....")

    input_dim = x_train.shape[1]
    nb_class = y_train.shape[1]

    if(model_file == None):
        model = get_model(x_train, y_train, nb_class, input_dim)
        exit()
    else:
        model = load_model(model_file)

    # features = Features(features_file)

    print(filetestConllu)
    obj_generateAlltree = ConstructAllTree(filetestConllu, get_mcd(), False)
    all_tree = obj_generateAlltree.get_allTree()

    features = Features(features_file)
    features.set_label_encoderX(labels_encoderX)
    features.set_label_encoderY(labels_encoderY)

    for id, tree in enumerate(all_tree):
        all_vertices = tree.get_vertices()[1:]
        liste_word = list()
        for index, vertice in enumerate(all_vertices):
            word = vertice.get_word()
            liste_word.append(word)
        print("INDEX=", id, " ", len(liste_word))

        A = Automate(model, features=features, sentence=liste_word)
        tree = A.run("Data/embd_fr_50.vec")

        print("tree=", tree)
        all_tree_automate.append(tree)

    print("Generation du fichier conllu....")

    TransformTreeConllu(all_tree, "generate_data.txt", filetestConllu)

    print("Scrip Evaluation ...")


if(__name__ == "__main__"):

    main("Data/test_conllu.txt", "Data/test_conllu.txt", "Data/f1_tbp.fm",
         file_genarate="generateFr_F1.conllu", model_file="test_model.h5")

    # model = load_model("models/model_fr_f1.h5")
    # X = np.load("models/data-fr-f1/X_f1_all.npy")
    # Y= np.load("models/data-fr-f1/Y_f1_all.npy")
    #
    # print(X.shape)
    # print(Y.shape)
    #
    # p = model.predict(X[0:10])
    #
    # print(p.shape)
    # print(p)
