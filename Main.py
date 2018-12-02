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
from Transform_Tree_Conllu import  *

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

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()[:1000]
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
    #
    print(features.datas)
    #
    # print(features.labels_encoders)



    print("Convertion du dataset")
    print("file_embedding : ", file_embedding)
    X, Y = features.get_Data_Set(file_embedding)

    """X_onehot = features.convert_datas_to_one_hot()

	Y_onehot = features.convert_labels_to_one_hot()"""
    return X, Y


def get_data(file_features, file_train_conllu, file_embedding=None):

    x_train, y_train = get_xy(file_train_conllu, file_features, file_embedding)

    return x_train, y_train


def get_model(x_train,y_train,nb_class,input_dim):
    model=create_neural_network_model (nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model.fit (x_train, y_train, epochs=10, verbose=0)


    return  model


def main(filetestConllu,filetesttxt,features_file,model_file = None):
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
    conllu_file="test.txt"
    # weight_embedding_file = "embd_file_vectors/embd.vec"

    x_train, y_train=get_data (features_file, conllu_file)


    all_tree_automate = list()

    print("Train model ....")

    input_dim=x_train.shape[1]
    nb_class = y_train.shape[1]

    if(model_file == None):
        print("Not None")
        model = get_model(x_train,y_train,nb_class,input_dim)
    else:
        model = models.load(model_file)




    try:
        conlluFile=open (filetesttxt, encoding='utf-8')
    except IOError:
        print ("erreur ouverture fichier", filetesttxt)
        exit (1)



    s=conlluFile.read ()
    conlluFile.close ()
    # création d'une liste contenant tout les ligne du fichier
    liste_lignes=s.splitlines ()

    print(liste_lignes[0])


    features = Features(features_file)


    print(filetestConllu)
    obj_generateAlltree = ConstructAllTree(filetestConllu, get_mcd(), False)
    all_tree = obj_generateAlltree.get_allTree()


    print("Taille de l'arbre =",len(all_tree))

    print("###########################################################""")

    for id,tree in enumerate(all_tree):
        all_vertices = tree.get_vertices()[1:]
        liste_word = list()
        for index, vertice in enumerate(all_vertices):
            word = vertice.get_word()
            liste_word.append(word)
        print("INDEX=",id," ",len(liste_word))
        A=Automate (model, features, liste_word)
        tree = A.run()
        print("tree=",tree)
        all_tree_automate.append (tree)

    exit()





    print("Generation du fichier conllu....")


    TransformTreeConllu (all_tree_automate, "generate_data.txt", "fr_gs-ud-test.conllu")


    print("Scrip Evaluation ...")

























if(__name__ == "__main__"):


    main("Data/fr_gsd-ud-test.conllu","Data/fr_gsd-ud-test.txt","Data/f1_tbp.fm")

    # features_file = "Data/f1_tbp.fm"
    # #conllu_file = "Data/fr_gsd-ud-train.conllu"
    # # conllu_file = "Data/fr_gsd-ud-train.conllu"
    # conllu_file = "test.txt"
    # # weight_embedding_file = "embd_file_vectors/embd.vec"
    #
    # x_train, y_train = get_data(
    #     features_file, conllu_file)
    # # x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
    # print("x_train=", x_train.shape)
    # print("X=",x_train[0])
    # print("Y_train=", y_train.shape)
    #
    # print("save file")
    # outfile_X = "X.npy"
    # outfile_Y = "Y.npy"
    # np.save(outfile_X, x_train)
    # np.save(outfile_Y, y_train)
    #
    # print("start_train")

    """input_dim = x_train.shape[1]
    print("input_dim= ", input_dim)
    nb_class = y_train.shape[1]
    print("nb_class= ", nb_class)

    model = create_neural_network_model(nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model1.fit(x_train, y_train, epochs=1000)

    """
    """score = model1.evaluate(x_test, y_test)
    print("%s: %.2f%%" % (model1.metrics_names[1], score[1] * 100))

    model.save('model_f2.h5')  # creates a HDF5 file 'my_model.h5'
    del model  # deletes the existing model"""
