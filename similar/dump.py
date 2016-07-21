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
from config import L18_deep_features_folder, slice_batch, slice_count, slice_dump_pattern, L18_image_list, slice_names_pattern, L18_tiles_number


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

db = leveldb.LevelDB(L18_deep_features_folder)

# load features
for idx in range(0, slice_count):
    min_count = idx * slice_batch
    max_count = (idx + 1) * slice_batch
    if max_count >= L18_tiles_number:
        max_count = L18_tiles_number

    print 'process slice #%d, range: %d - %d' % (idx, min_count, max_count)

    count = 0
    keys = list()
    features = list()
    for key, value in db.RangeIter():
        if count < min_count:
            count += 1
            continue

        if count >= max_count:
            break

        datum = caffe_pb2.Datum.FromString(db.Get(key))
        data = caffe.io.datum_to_array(datum)
        feat = np.transpose(data[:, 0])[0]
        keys.append(key)
        features.append(feat)

        count += 1
        if count % 1000 == 0:
            print 'process slice #%d, range: %d - %d' % (idx, min_count, max_count)
            print 'processed %d' % (count)

    features = np.array(features)
    print len(features)
    print len(features[0])

    image_names_txt = '%s_%d.txt' % (slice_names_pattern, idx)
    print 'write image names lookup %s' % (image_names_txt)
    ff = open(image_names_txt, 'w')

    with open(L18_image_list, 'r') as f:
        count = 0
        for line in f:
            if count < min_count:
                count += 1
                continue

            if count >= max_count:
                break

            file_path, x, y = line.strip().split()
            filename = x + '_' + y
            ff.write(filename)
            ff.write('\n')

            count += 1
    ff.close()

    dump_file = '%s_%d.dat' % (slice_dump_pattern, idx)
    print 'write dump files %s' % (dump_file)
    convert_to_cov_format(features, dump_file, 'all')
