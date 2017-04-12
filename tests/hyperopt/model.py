from __future__ import print_function

from deepcpg.utils import get_from_module
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.datasets import imdb

# set parameters:


def build_model(max_features=5000, maxlen=400,
                batch_size=32, embedding_dims=50,
                filters=250, kernel_size=3, hidden_dims=250):
    print('Build model...')
    model = Sequential()

    # we start off with an efficient embedding layer which maps
    # our vocab indices into embedding_dims dimensions
    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))
    model.add(Dropout(0.2))

    # we add a Convolution1D, which will learn filters
    # word group filters of size filter_length:
    model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
    # we use max pooling:
    model.add(GlobalMaxPooling1D())

    # We add a vanilla hidden layer:
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))

    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
    # model.fit(x_train, y_train,
    #           batch_size=batch_size,
    #           epochs=epochs,
    #           validation_data=(x_test, y_test))

def hyperopt_loss_build_model(x):
    return x[0]

def update_param_build_model(x, train):
    return x

# --------------------------------------------

def get(name):
    return get_from_module(name, globals())


def get_loss(name):
    try:
        return get_from_module("hyperopt_loss_" + name, globals())
    except Exception:
        return lambda x: x[0]

def get_update_param(name):
    try:
        return get_from_module("update_param_" + name, globals())
    except Exception:
        return lambda x: x
