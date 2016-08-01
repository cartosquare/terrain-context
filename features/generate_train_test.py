import numpy as np
from sklearn.cross_validation import train_test_split
import cPickle
import pandas as pd
from itertools import compress

# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import caffe_root, deep_features_folder, x_train_file, x_test_file, y_train_file, y_test_file, image_list_txt, debug, tags_number
sys.path.insert(0, caffe_root + 'python')

import caffe
import leveldb
from caffe.proto import caffe_pb2

db = leveldb.LevelDB(deep_features_folder)

# load features
count = 1
keys = list()
features = list()
for key, value in db.RangeIter():
    datum = caffe_pb2.Datum.FromString(db.Get(key))
    data = caffe.io.datum_to_array(datum)
    feat = np.transpose(data[:, 0])[0]
    keys.append(key)
    features.append(feat)

    count += 1
    if count % 100 == 0:
        print 'processed %d' % (count)

features = np.array(features)
print len(features)
print len(features[0])

image_list = pd.read_csv(image_list_txt, header=None, names=['path', 'label'], delimiter=' ')
print image_list.columns
print image_list.shape

X_train = list()
X_test = list()
y_train = list()
y_test = list()

first_label = True
for label in range(0, tags_number):
    # extract train and test set for each label
    mask = (image_list['label'] == label)
    print '#label: %d, #samples: %d' % (label, np.sum(mask))

    # check this !!!
    sub_features = list(compress(features, mask.values.tolist()))
    sub_labels = image_list['label'][mask].values.tolist()
    X_train_sub, X_test_sub, y_train_sub, y_test_sub = train_test_split(sub_features, sub_labels, test_size=0.4, random_state=42)

    print '#x_train: %d, #x_test: %d, #y_train: %d, y_test: %d' % (len(X_train_sub), len(X_test_sub), len(y_train_sub), len(y_test_sub))

    if first_label:
        first_label = False
        X_train = X_train_sub
        X_test = X_test_sub
        y_train = y_train_sub
        y_test = y_test_sub
    else:
        X_train = np.row_stack((X_train, X_train_sub))
        X_test = np.row_stack((X_test, X_test_sub))
        y_train = y_train + y_train_sub
        y_test = y_test + y_test_sub


print 'train split: '
print 'train simension: %d, %d' % (len(X_train), len(X_train[0]))
print 'test simension: %d, %d' % (len(X_test), len(X_test[0]))
print 'label split: '
print len(y_train)
print len(y_test)

with open(x_train_file, 'wb') as f:
    cPickle.dump(X_train, f, -1)
with open(x_test_file, 'wb') as f:
    cPickle.dump(X_test, f, -1)

with open(y_train_file, 'wb') as f:
    cPickle.dump(y_train, f, -1)
with open(y_test_file, 'wb') as f:
    cPickle.dump(y_test, f, -1)

# debug
if debug:
    with open(x_train_file, 'rb') as f:
        x_train_valid = cPickle.load(f)
        print 'validate train simension: %d, %d' % (x_train_valid.shape[0], x_train_valid.shape[1])
    with open(x_test_file, 'rb') as f:
        x_test_valid = cPickle.load(f)
        print 'validate test simension: %d, %d' % (x_test_valid.shape[0], x_test_valid.shape[1])
    with open(y_train_file, 'rb') as f:
        y_train_valid = cPickle.load(f)
        print len(y_train_valid)
    with open(y_test_file, 'rb') as f:
        y_test_valid = cPickle.load(f)
        print len(y_test_valid)
