"""
Main classe Principale
"""

from ConstructAllTree import *
from Features import  *

from Oracle import *



def get_mcd(self):
    self.mcd = (
        ('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
        ('GOV', 'SYM'),
        ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    return self.mcd

def set_mcd(self,mcd):
    self.mcd = mcd



def get_data(self,file_features,file_train_conllu,file_test_conllu):


    # Test de la classe Oracle et Features

    # Lecture du fichier conllu
    obj_generateAlltree = ConstructAllTree("test.txt", mcd, False)
    all_tree = obj_generateAlltree.get_allTree()

    features = Features("Data/f3_tbp.fm")

    for tree in all_tree:
        # tree.print_tree()

        A = Oracle(tree, features)

        result_tree = A.run()
    # result_tree.print_tree()

    print("Liste des données (X) :")
    print(features.datas)
    print("Liste des labels (Y) :")
    print(features.labels)
    print("Nb label : ", len(features.labels))
    print("Nb data : ", len(features.datas))

    onehot = features.convert_datas_to_one_hot()
    print("Final ", onehot)