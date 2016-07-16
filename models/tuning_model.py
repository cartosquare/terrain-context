# -*- coding: utf-8 -*-
import numpy as np
from hyperopt import hp
from hyperopt import fmin, tpe, Trials

## keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils, generic_utils

import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

# serialization
import cPickle

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import x_train_file, x_test_file, y_train_file, y_test_file, tags_number


def score(param):
    hidden_units = int(param["hidden_units"])

    ## regression with keras' deep neural networks
    model = Sequential()

    ## hidden layers
    hidden_layers = int(param['hidden_layers'])
    first_layer = True
    while hidden_layers > 0:
        # Dense layer
        if first_layer:
            model.add(Dense(hidden_units, input_dim=X_train.shape[1], init='glorot_uniform'))
        else:
            model.add(Dense(hidden_units, init='glorot_uniform'))

        # batch normal
        if param["batch_norm"]:
            model.add(BatchNormalization(input_shape=(hidden_units,)))

        # Activation layer
        if param["hidden_activation"] == "prelu":
            model.add(PReLU(input_shape=(hidden_units,)))
        else:
            model.add(Activation(param['hidden_activation']))

        # dropout layer
        if first_layer:
            first_layer = False
            model.add(Dropout(param["input_dropout"]))
        else:
            model.add(Dropout(param["hidden_dropout"]))

        hidden_layers -= 1

    ## output layer
    model.add(Dense(tags_number, init='glorot_uniform'))
    model.add(Activation(param['output_activation']))

    ## loss
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    ## train
    # model.fit(X_train, Y_train, nb_epoch=int(param['nb_epoch']), batch_size=int(param['batch_size']), validation_data=(X_test, Y_test), shuffle=True)
    model.fit(X_train, Y_train, nb_epoch=int(param['nb_epoch']), batch_size=int(param['batch_size']), validation_split=0, verbose=0, shuffle=True)

    ## prediction
    pred = model.predict(X_test, verbose=0)
    correct = 0
    for row in range(0, len(pred)):
        a = list(pred[row])
        b = sorted(range(len(a)), key=lambda i: a[i])[-5:]

        if y_test[row] in b:
            correct += 1

    top_5_error = 1 - float(correct) / float(len(y_test))
    print 'top-5 error: %f' % (top_5_error)

    return top_5_error


def optimize(trials):
    space = {
        "batch_norm": hp.choice("batch_norm", [True, False]),
        "hidden_units": hp.choice("hidden_units", [64, 128, 256, 512]),
        "hidden_layers": hp.choice("hidden_layers", [1, 2, 3, 4]),
        "input_dropout": hp.quniform("input_dropout", 0, 0.9, 0.1),
        "hidden_dropout": hp.quniform("hidden_dropout", 0, 0.9, 0.1),
        "hidden_activation": hp.choice("hidden_activation", ["relu", "prelu", "sigmoid"]),
        "output_activation": hp.choice("output_activation", ["relu", "sigmoid"]),
        "batch_size": hp.choice("batch_size", [16, 32, 64, 128, 256, 512, 1024]),
        "nb_epoch": hp.choice("nb_epoch", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    }

    best = fmin(score, space, algo=tpe.suggest, trials=trials, max_evals=300)

    return best

# loading data
with open(x_train_file, 'rb') as f:
    X_train = cPickle.load(f)
with open(x_test_file, 'rb') as f:
    X_test = cPickle.load(f)
with open(y_train_file, 'rb') as f:
    y_train = cPickle.load(f)
with open(y_test_file, 'rb') as f:
    y_test = cPickle.load(f)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, tags_number)
Y_test = np_utils.to_categorical(y_test, tags_number)

# Trials object where the history of search will be stored
trials = Trials()

best_param = optimize(trials)
print best_param

score(best_param)
