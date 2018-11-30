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

    all_tree = obj_generateAlltree.get_allTreeProjectiviser()[:200]
    print(all_tree)
    #
    features = Features(file_features)
    for tree in all_tree:
        # tree.print_tree()

        A = Oracle(tree, features)

        A.run()

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


    # Lecture du fichier conllu

    x_train,y_train = get_xy(file_train_conllu,file_features)
    # x_test,y_test = get_xy(file_test_conllu,file_features)


    return x_train,y_train,




x_train,y_train = get_data("Data/f1_tbp.fm","test.txt","test.txt")
# x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
print("X_train=",x_train)
print("X_train=",y_train)

