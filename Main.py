"""
Main classe Principale
"""

from ConstructAllTree import *
from Features import  *

from Oracle import *



def get_mcd():
    mcd = (
        ('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
        ('GOV', 'SYM'),
        ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    return mcd

def set_mcd(mcd):
    mcd = mcd



def get_xy(file_conllu,file_features):
    mcd = get_mcd()
    obj_generateAlltree = ConstructAllTree(file_conllu, mcd, True)

    all_tree = obj_generateAlltree.get_allTree()
    print(all_tree)
    exit()

    features = Features(file_features)

    for tree in all_tree:
        # tree.print_tree()

        A = Oracle(tree, features)

        result_tree = A.run()
    # # result_tree.print_tree()
    #
    # print("Liste des données (X) :")
    # print(features.datas)
    # print("Liste des labels (Y) :")
    # print(features.labels)
    # print("Nb label : ", len(features.labels))
    # print("Nb data : ", len(features.datas))
    #
    # onehot = features.convert_datas_to_one_hot()
    # print("Final ", onehot)

    return features.datas,features.labels

def get_data(file_features,file_train_conllu,file_test_conllu):


    # Test de la classe Oracle et Features

    # Lecture du fichier conllu

    x_train,y_train = get_xy(file_train_conllu,file_features)
    x_test,y_test = get_xy(file_test_conllu,file_features)


    return x_train,x_test,y_train,y_test




x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","Data/fr_gsd-ud-train.conllu","Data/fr_gsd-ud-test.conllu")

print("X_train=",x_train)
print("X_test=",x_test)
print("X_train=",y_train)
print("X_test=",y_test)