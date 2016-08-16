## keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils, generic_utils
from keras.models import model_from_json
import numpy as np
import cPickle
import pandas as pd
import os
import sys
# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
caffe_root = '../caffe/'
sys.path.insert(0, caffe_root + 'python')

import caffe
import leveldb
from caffe.proto import caffe_pb2

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import L18_deep_features_folder, slice_batch, slice_count, slice_dump_pattern, L18_image_list, slice_names_pattern, L18_tiles_number, model_architecture_file, model_weights_file


def get_file_with_parents(filepath, levels=1):
    common = filepath
    for i in range(levels + 1):
        common = os.path.dirname(common)
    return os.path.relpath(filepath, common)


def convert_to_cov_format(in_arr, filepath, count):
    with open(filepath, 'w') as f:
        if in_arr.dtype != np.dtype('float64'):
            in_arr = in_arr.astype('float64')
            if count != 'all':
                in_arr = in_arr[:int(count)]
        n_points = np.array(in_arr.shape[0], dtype='int32')
        n_points.tofile(f)
        dims = np.array(in_arr.shape[1], dtype='int32')
        dims.tofile(f)
        in_arr.tofile(f)

# load model
print model_architecture_file
model = model_from_json(open(model_architecture_file).read())
print model_weights_file
model.load_weights(model_weights_file)

# Finally, before it can be used, the model shall be compiled.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print L18_deep_features_folder
db = leveldb.LevelDB(L18_deep_features_folder)
count = 0
keys = list()
features = list()
for key, value in db.RangeIter():
    if count >= L18_tiles_number:
        break

    datum = caffe_pb2.Datum.FromString(db.Get(key))
    data = caffe.io.datum_to_array(datum)
    feat = np.transpose(data[:, 0])[0]
    feat = np.array([feat])
    feat = feat.astype('float32')

    keys.append(key)

    # calculate prob
    pred = model.predict(feat)
    features.append(pred[0])

    count += 1
    if count % 1000 == 0:
        print pred[0].shape
        print 'processed %d' % (count)

features = np.array(features)
print len(features)
print len(features[0])

image_names_txt = '%s_%d.txt' % (slice_names_pattern, 0)
print 'write image names lookup %s' % (image_names_txt)
ff = open(image_names_txt, 'w')

with open(L18_image_list, 'r') as f:
    count = 0
    for line in f:
        file_path, label = line.strip().split()

        rel_path = get_file_with_parents(file_path, 1)
        y = str(rel_path).split('/')[0]

        base = os.path.basename(file_path)
        x = os.path.splitext(base)[0]

        filename = x + '_' + y

        ff.write(filename)
        ff.write('\n')

        count += 1
    print 'processed %d image filename' % (count)
ff.close()

dump_file = '%s_%d.dat' % (slice_dump_pattern, 0)
print 'write dump files %s' % (dump_file)
convert_to_cov_format(features, dump_file, 'all')
