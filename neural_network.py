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


def create_neural_network_model(num_classes, input_dim):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=input_dim))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


if(__name__ == "__main__"):
    X_file = "npy_model/X_f1_fr.npy"
    Y_file = "npy_model/Y_f1_fr.npy"
    x_train = np.load(X_file, mmap_mode='r')
    y_train = np.load(Y_file, mmap_mode='r')
    print("start_train")
    input_dim = x_train.shape[1]
    print("input_dim= ", input_dim)
    nb_class = y_train.shape[1]
    print("nb_class= ", nb_class)
    model = create_neural_network_model(nb_class, input_dim)
    # Train the model, iterating on the data in batches of 32 samples
    model.fit(x_train, y_train, epochs=50, batch_size=20)

    """score = model1.evaluate(x_test, y_test)
    print("%s: %.2f%%" % (model1.metrics_names[1], score[1] * 100))"""

    model.save('model_f1_FR.h5')  # creates a HDF5 file 'my_model.h5'
    del model  # deletes the existing model"""
