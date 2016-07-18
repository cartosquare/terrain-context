# -*- coding: utf-8 -*-

## keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils, generic_utils

# measure time
import time
# serialization
import cPickle

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import x_train_file, x_test_file, y_train_file, y_test_file, tags_number

import pandas as pd

# loading data
with open(x_train_file, 'rb') as f:
    X_train = cPickle.load(f)
with open(x_test_file, 'rb') as f:
    X_test = cPickle.load(f)
with open(y_train_file, 'rb') as f:
    y_train = cPickle.load(f)
with open(y_test_file, 'rb') as f:
    y_test = cPickle.load(f)

print(X_train.shape[0], X_train.shape[1], 'train samples')
print(X_test.shape[0], X_test.shape[1], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, tags_number)
Y_test = np_utils.to_categorical(y_test, tags_number)

# a simple two-layer network
model = Sequential()
model.add(Dense(256, input_dim=X_train.shape[1], init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(256,)))
model.add(Activation('relu'))
model.add(Dropout(0.7))

model.add(Dense(tags_number))
model.add(Activation('sigmoid'))

## loss
# try rmsprop
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

## train
start = time.time()

# fit
model.fit(X_train, Y_train, nb_epoch=30, batch_size=16, shuffle=True)

# evaluate
score, acc = model.evaluate(X_test, Y_test, batch_size=16)
print 'top-1 error: %f' % (acc)

# predict
pred = model.predict(X_test)
correct = 0
for row in range(0, len(pred)):
    a = list(pred[row])
    b = sorted(range(len(a)), key=lambda i: a[i])[-5:]

    if y_test[row] in b:
        correct += 1

top_5_error = 1 - float(correct) / float(len(y_test))
print 'top-5 error: %f' % (top_5_error)

end = time.time()
print('Time elapsed: %f' % (end - start))
