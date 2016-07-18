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
from config import x_train_file, x_test_file, y_train_file, y_test_file, tags_number, unique_tags_csv


def show_top5_error():
    # label-lookup
    labels_loopup = []
    count = 0
    with open(unique_tags_csv) as f:
        for line in f:
            (tag, tag_cn, label) = line.strip().split(',')
            if count != int(label):
                print 'invalid label loopup!'
            labels_loopup.append(tag_cn)
            count = count + 1

    correct = 0
    good_predict = []
    bad_predict = []
    for i in range(0, tags_number):
        good_predict.append(0)
        bad_predict.append(0)

    for row in range(0, len(pred)):
        a = list(pred[row])
        b = sorted(range(len(a)), key=lambda i: a[i])[-5:]

        if y_test[row] in b:
            correct += 1
            good_predict[y_test[row]] += 1
        else:
            bad_predict[y_test[row]] += 1

    top_5_error = 1 - float(correct) / float(len(y_test))
    print 'top-5 error: %f' % (top_5_error)

    class_errors = []
    for i in range(0, tags_number):
        scores = float(bad_predict[i]) / float((bad_predict[i] + good_predict[i]))
        class_errors.append(scores)

    sorted_errors = sorted(range(len(class_errors)), key=lambda k: class_errors[k])

    for i in range(1, tags_number + 1):
        idx = tags_number - i
        print 'label %d - %s top-5 error: %f' % (sorted_errors[idx], labels_loopup[sorted_errors[idx]], class_errors[sorted_errors[idx]])

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

# {'hidden_units': 512, 'hidden_activation': 'relu', 'batch_size': 32, 'input_dropout': 0.2, 'hidden_dropout': 0.1, 'output_activation': 'sigmoid', 'hidden_layers': 6, 'nb_epoch': 30, 'batch_norm': True}
hidden_unit = 512
model.add(Dense(hidden_unit, input_dim=X_train.shape[1], init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(hidden_unit, init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(hidden_unit, init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(hidden_unit, init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(hidden_unit, init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(hidden_unit, init='glorot_uniform'))
model.add(BatchNormalization(input_shape=(hidden_unit,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

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
model.fit(X_train, Y_train, nb_epoch=30, batch_size=32, shuffle=True)

end = time.time()
print('Training Time: %f' % (end - start))

# evaluate
score, acc = model.evaluate(X_test, Y_test, batch_size=32)
print '\ntop-1 error: %f' % (acc)

# predict
pred = model.predict(X_test)
show_top5_error()
