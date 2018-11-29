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
