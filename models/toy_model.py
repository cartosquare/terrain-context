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


# loading data
with open(x_train_file, 'rb') as f:
    X_train = cPickle.load(f)
with open(x_test_file, 'rb') as f:
    X_test = cPickle.load(f)
with open(y_train_file, 'rb') as f:
    y_train = cPickle.load(f)
with open(y_test_file, 'rb') as f:
    y_test = cPickle.load(f)

print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, tags_number)
Y_test = np_utils.to_categorical(y_test, tags_number)

# a simple two-layer network
model = Sequential()
model.add(Dense(256, activation='relu', input_dim=X_train.shape[1], init='glorot_uniform'))
model.add(Dropout(0.5))
model.add(Dense(tags_number, activation='sigmoid'))

## loss
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

## train
start = time.time()

model.fit(X_train, Y_train, nb_epoch=10, batch_size=32, validation_data=(X_test, Y_test), shuffle=True)

end = time.time()
print('Time elapsed: %f' % (end - start))
