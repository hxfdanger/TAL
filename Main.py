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
		('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA','INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
		('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

	return mcd


def set_mcd(mcd):
	mcd = mcd


def get_xy(file_conllu, file_features):
	mcd = get_mcd()

	print("Chargement des arbres")
	obj_generateAlltree = ConstructAllTree(file_conllu, mcd, True)
	all_tree = obj_generateAlltree.get_allTreeProjectiviser()
	#print(all_tree[0].print_tree())
	print("Arbres charger : ",len(all_tree))

	print("Création du dataset")
	features = Features(file_features)
	i = 0
	for tree in all_tree:
		print(i)
		i+=1
		tree.print_tree()
		
		A = Oracle(tree, features)
		A.run()

	print("Convertion du dataset")
	print(features)

	# X_onehot=features.convert_datas_to_one_hot ()
	# Y_onehot = features.convert_labels_to_one_hot()
	#
	# return X_onehot, Y_onehot



def get_data(file_features, file_train_conllu, file_test_conllu):

	# Test de la classe Oracle et Features

	# Lecture du fichier conllu


	x_train, y_train = get_xy(file_train_conllu, file_features)
	# x_test, y_test = get_xy(file_test_conllu, file_features)

	return x_train, y_train


if(__name__ == "__main__"):


	# On', 'ne', 'peut', 'éviter', 'de', 'penser', 'à', "l'", 'actualité', 'caractérisée', 'par', "l'", 'enlèvement', 'de', 'les', 'otages', 'à', 'le', 'Niger'


	x_train, y_train = get_data( "Data/f1_tbp.fm", "Data/fr_gsd-ud-train.conllu", "Data/fr_gsd-ud-test.conllu")
	# x_train,x_test,y_train,y_test = get_data("Data/f1_tbp.fm","test.txt","test.txt")
	print("X_train=", x_train.shape)
	print("Y_train=", y_train.shape)
