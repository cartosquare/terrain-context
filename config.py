"""
__file__

    config.py

__description__

    This file provides global parameter configurations for the project.

__author__

    atlasxu < xux@geohey.com >

"""

import math
from hyperopt import hp

# Parameters that you must pay attention to:

## debug switch
## Warning: changing debug to True will not let caffe extract_feature
## to process image_list_test.txt, if you want do so, change corresponding
## model prototex file
debug = False

# tags file name
tag_file_name = 'tags_70'

# #tiles in level 18
L18_tiles_number = 2349583

# number of training tiles
training_tiles_number = 71244

if debug:
    tags_number = 2
else:
    tags_number = 70

# osm pbf format data
pbf_file = '/Users/xuxiang/mapping/g-map/set_up_osm_data/china-latest.osm.pbf'

# google static map api key
KEY = 'AIzaSyDjldHb_52Ui1etlmLORjFS_5xZv3yMjNg'

## general folders

# osm tags folder
osm_tags_folder = './osm_tags'

# google image downloading folder
images_folder = './images'

# features folder
features_folder = './features'

# models folder
models_folder = './models'

# similar folder
similar_folder = './similar'

## osm tags

# node tags csv
osm_node_tags_csv = osm_tags_folder + '/node_tags.csv'

# way tags csv
osm_way_tags_csv = osm_tags_folder + '/way_tags.csv'

if debug:
    postfix = '_test'
else:
    postfix = ''

# csv that combines node and way tags
all_tags_csv = osm_tags_folder + '/%s%s.csv' % (tag_file_name, postfix)

# subset of all tags(This is the tags that we want to learn)
tags_csv = osm_tags_folder + '/%s_subset%s.csv' % (tag_file_name, postfix)

# in tags_csv file, a tag may occurs two times(both as node and way tags)
# in this file, we list all the unique tags
unique_tags_csv = osm_tags_folder + '/%s_map%s.csv' % (tag_file_name, postfix)

# extracted data by tags
tags_node_data_folder = osm_tags_folder + '/tags_node_data%s' % (postfix)
tags_way_data_folder = osm_tags_folder + '/tags_way_data%s' % (postfix)

# download list contains all the coordinates of corresponding tags
# in later works, we will download an image for each pair of coordinate
download_list_csv = osm_tags_folder + '/%s_download_list%s.csv' % (tag_file_name, postfix)

# downloading parameters
if debug:
    samples_per_category = 10
else:
    samples_per_category = 5000

# space for discrect way features
# Calculated for latitude 25.769322
lng_offset = 0.000853
lat_offset = 0.000686


## images

# image parameters
image_size = 256
default_zoom = 18
bottom_crop = 23
min_samples_per_category = samples_per_category / 2

# image folder
google_image_folder = images_folder + '/%s_tiles%s' % (tag_file_name, postfix)
# L18_image_folder = images_folder + '/L18_google_images%s' % (postfix)
L18_image_folder = images_folder + '/google_images_test'

## features

# image list
image_list_txt = features_folder + '/%s_image_list%s.txt' % (tag_file_name, postfix)
L18_image_list = features_folder + '/image_list_L18%s.txt' % (postfix)
L18_keys_file = features_folder + '/L18_keys%s' % (postfix)

# caffe binary
caffe_root = '../caffe/'
caffe_extract_features_bin = '../caffe/build/tools/extract_features.bin'

# caffe model, can be resnet or bvlc
caffemodel = 'bvlc'

if caffemodel == 'resnet':
    ## deep-residual-networks
    caffe_model_file = './resnet/ResNet-50-model.caffemodel'
    caffe_proto_text = './resnet/ResNet-50-deploy.prototxt'
    blob_name = 'fc1000'
else:
    # caffe bvlc model
    caffe_model_file = './caffenet/bvlc_reference_caffenet.caffemodel'
    caffe_proto_text = './caffenet/imagenet_val.prototxt'
    caffe_proto_L18_text = './caffenet/imagenet_val_L18.prototxt'
    blob_name = 'fc7'

use_gpu = False

# deep feature folder
deep_features_folder = features_folder + '/%s_deep_features_%s_%s%s' % (tag_file_name, caffemodel, blob_name, postfix)
L18_deep_features_folder = features_folder + '/L18_deep_features_%s%s' % (caffemodel, postfix)

# batchs when calculating deep feature
feature_batch = 50
extract_feature_batch = int(math.ceil(float(training_tiles_number) / float(feature_batch)))

# training-validating sample files
x_train_file = features_folder + '/%s_x_train_%s_%s%s.pkl' % (tag_file_name, caffemodel, blob_name, postfix)
x_test_file = features_folder + '/%s_x_test_%s_%s%s.pkl' % (tag_file_name, caffemodel, blob_name, postfix)
y_train_file = features_folder + '/%s_y_train_%s_%s%s.pkl' % (tag_file_name, caffemodel, blob_name, postfix)
y_test_file = features_folder + '/%s_y_test_%s_%s%s.pkl' % (tag_file_name, caffemodel, blob_name, postfix)


## models
debug_model = False
model_architecture_file = models_folder + '/%s_model_architecture_%s_%s%s.json' % (tag_file_name, caffemodel, blob_name, postfix)
model_weights_file = models_folder + '/%s_model_weights_%s_%s%s.h5' % (tag_file_name, caffemodel, blob_name, postfix)

if debug_model:
    space = {
        'batch_norm': hp.choice('batch_norm', [True, False]),
        'hidden_units': hp.choice('hidden_units', [16, 32, 64]),
        'hidden_layers': hp.choice('hidden_layers', [1, 2, 3]),
        'input_dropout': hp.quniform('input_dropout', 0, 0.9, 0.1),
        'hidden_dropout': hp.quniform('hidden_dropout', 0, 0.9, 0.1),
        'hidden_activation': hp.choice('hidden_activation', ['relu', 'prelu', 'sigmoid']),
        'output_activation': hp.choice('output_activation', ['relu', 'sigmoid']),
        'batch_size': hp.choice('batch_size', [16, 32, 64]),
        'nb_epoch': hp.choice('nb_epoch', [5, 10, 20])
    }
    max_evaluate = 2
    verbose_output = 1
else:
    space = {
        'input_dropout': hp.quniform('input_dropout', 0, 0.9, 0.01),
        'hidden_dropout': hp.quniform('hidden_dropout', 0, 0.9, 0.01),
        'batch_size': hp.choice('batch_size', [16, 32, 64, 128]),
        'nb_epoch': hp.choice('nb_epoch', [10, 20, 30, 40, 50])
    }
    max_evaluate = 100
    verbose_output = 0

## similar
slice_batch = 250000
slice_dump_pattern = similar_folder + '/slice_dump'
slice_names_pattern = similar_folder + '/slice_name'

slice_count = int(math.ceil(float(L18_tiles_number) / float(slice_batch)))
