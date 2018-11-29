# neurone NW
# entré
#
from keras.utils.np_utils import to_categorical
from sklearn import preprocessing
import numpy as np
from ConstructAllTree import ConstructAllTree
from Features import Features
from Oracle import Oracle
from keras.models import Sequential
from keras.layers import Dense, Activation
from numpy import argmax

import keras


# Test de la classe Oracle et Features
mcd = (('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'),
       ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

# Lecture du fichier conllu
obj_generateAlltree = ConstructAllTree(
    "test_conllu.txt", mcd, False)
all_tree = obj_generateAlltree.get_allTree()

features = Features("f1_tbp.fm")

for tree in all_tree:
    # tree.print_tree()

    A = Oracle(tree, features)
    result_tree = A.run()
    # result_tree.print_tree()
"""print("Liste des données (X) :")
print(features.datas[1])
print("Liste des labels (Y) :")
print(features.labels[1])
print("Nb label : ", len(features.labels))
print("Nb data : ", len(features.datas))"""

"""X_train = features.convert_datas_to_one_hot()
print(X_train[1])
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
# to use LabelEncoder
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
Y_train = to_categorical(Y1, nb_class)
print(Y_train)
# reverse to_categorical
Y2 = argmax(Y_train, axis=1)
print(Y2)
# reverse LabelEncoder
Y3 = le.inverse_transform(Y2)
print(Y3)"""


def create_neural_network_model(num_classes, input_dim):
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=input_dim))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


if(__name__ == "__main__"):
    input_dim = X_train.shape[1]
    model1 = create_neural_network_model(nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model1.fit(X_train, Y_train, epochs=1000)
    score = model1.evaluate(X_train, Y_train)
    print("%s: %.2f%%" % (model1.metrics_names[1], score[1] * 100))
    print("loss %f.2" % score[0])
