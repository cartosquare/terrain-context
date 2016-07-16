# -*- coding: utf-8 -*-
# hyperopt
import hyperopt
from hyperopt import fmin, tpe, Trials

## keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils, generic_utils

# serialization
import cPickle

# configure
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import x_train_file, x_test_file, y_train_file, y_test_file, tags_number, space, max_evaluate, verbose_output


def optimize(trials):
    best = fmin(score, space, algo=tpe.suggest, trials=trials, max_evals=max_evaluate)
    return best


def score(param):
    hidden_units = int(param['hidden_units'])

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
        if param['batch_norm']:
            model.add(BatchNormalization(input_shape=(hidden_units,)))

        # Activation layer
        if param['hidden_activation'] == 'prelu':
            model.add(PReLU(input_shape=(hidden_units,)))
        else:
            model.add(Activation(param['hidden_activation']))

        # dropout layer
        if first_layer:
            first_layer = False
            model.add(Dropout(param['input_dropout']))
        else:
            model.add(Dropout(param['hidden_dropout']))

        hidden_layers -= 1

    ## output layer
    model.add(Dense(tags_number, init='glorot_uniform'))
    model.add(Activation(param['output_activation']))

    ## loss
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    ## train
    # model.fit(X_train, Y_train, nb_epoch=int(param['nb_epoch']), batch_size=int(param['batch_size']), validation_data=(X_test, Y_test), shuffle=True)
    model.fit(X_train, Y_train, nb_epoch=int(param['nb_epoch']), batch_size=int(param['batch_size']), validation_split=0, verbose=verbose_output, shuffle=True)

    ## prediction
    pred = model.predict(X_test, verbose=verbose_output)

    ## calculate top-5 error
    correct = 0
    for row in range(0, len(pred)):
        a = list(pred[row])
        b = sorted(range(len(a)), key=lambda i: a[i])[-5:]

        if y_test[row] in b:
            correct += 1

    top_5_error = 1 - float(correct) / float(len(y_test))
    print 'top-5 error: %f' % (top_5_error)

    return top_5_error

## Program starts from here ...

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
best_param = hyperopt.space_eval(space, best_param)
print best_param

# run with best prameters
score(best_param)
