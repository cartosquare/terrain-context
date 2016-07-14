import numpy as np
from sklearn.cross_validation import train_test_split
import cPickle

# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import caffe_root, deep_features_folder, x_train_file, x_test_file, y_train_file, y_test_file, image_list_txt, debug
sys.path.insert(0, caffe_root + 'python')

import caffe
import leveldb
from caffe.proto import caffe_pb2

db = leveldb.LevelDB(deep_features_folder)

# load features
count = 1
keys = list()
for key, value in db.RangeIter():
    datum = caffe_pb2.Datum.FromString(db.Get(key))
    data = caffe.io.datum_to_array(datum)
    feat = np.transpose(data[:, 0])[0]
    keys.append(key)
    if count == 1:
        features = feat
        count += 1
    else:
        features = np.row_stack((features, feat))
print features.shape
# print features[12]

labels = list()
with open(image_list_txt) as f:
    for line in f:
        (filename, label) = line.strip().split()
        labels.append(label)

print len(labels)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25, random_state=42)

print X_train.shape
print len(y_train)
print X_test.shape
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
        print x_train_valid.shape
    with open(x_test_file, 'rb') as f:
        x_test_valid = cPickle.load(f)
        print x_test_valid.shape
    with open(y_train_file, 'rb') as f:
        y_train_valid = cPickle.load(f)
        print len(y_train_valid)
    with open(y_test_file, 'rb') as f:
        y_test_valid = cPickle.load(f)
        print len(y_test_valid)
