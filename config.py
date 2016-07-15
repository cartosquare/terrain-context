### This file contains all the configure parameters we need.
import math

## general folders

## debug switch
## Warning: changing debug to True will not let caffe extract_feature
## to process image_list_test.txt, if you want do so, change corresponding
## model prototex file
debug = False

# osm tags folder
osm_tags_folder = './osm_tags'

# google image downloading folder
images_folder = './images'

# features folder
features_folder = './features'

## osm tags

# osm pbf format data
pbf_file = '/Users/xuxiang/mapping/g-map/set_up_osm_data/china-latest.osm.pbf'

# node tags csv
osm_node_tags_csv = osm_tags_folder + '/node_tags.csv'

# way tags csv
osm_way_tags_csv = osm_tags_folder + '/way_tags.csv'

if debug:
    postfix = '_test'
else:
    postfix = ''

# csv that combines node and way tags
all_tags_csv = osm_tags_folder + '/all_tags%s.csv' % (postfix)

# subset of all tags(This is the tags that we want to learn)
tags_csv = osm_tags_folder + '/tags%s.csv' % (postfix)


# in tags_csv file, a tag may occurs two times(both as node and way tags)
# in this file, we list all the unique tags
unique_tags_csv = osm_tags_folder + '/unique_tags%s.csv' % (postfix)

# extracted data by tags
tags_node_data_folder = osm_tags_folder + '/tags_node_data%s' % (postfix)
tags_way_data_folder = osm_tags_folder + '/tags_way_data%s' % (postfix)

# download list contains all the coordinates of corresponding tags
# in later works, we will download an image for each pair of coordinate
download_list_csv = osm_tags_folder + '/download_list%s.csv' % (postfix)

# downloading parameters
if debug:
    samples_per_category = 10
else:
    samples_per_category = 500

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
KEY = 'AIzaSyDjldHb_52Ui1etlmLORjFS_5xZv3yMjNg'

# image folder
google_image_folder = images_folder + '/google_images%s' % (postfix)


## features

# image list
image_list_txt = features_folder + '/image_list%s.txt' % (postfix)

# caffe binary
caffe_root = '../caffe/'
caffe_extract_features_bin = '../caffe/build/tools/extract_features.bin'

# caffe model, can be resnet or bvlc
caffemodel = 'bvlc'

if caffemodel == 'resnet':
    ## deep-residual-networks
    caffe_model_file = './resnet/ResNet-152-model.caffemodel'
    caffe_proto_text = './resnet/ResNet-152-deploy.prototxt'
    blob_name = 'fc1000'
else:
    # caffe bvlc model
    caffe_model_file = './caffenet/bvlc_reference_caffenet.caffemodel'
    caffe_proto_text = './caffenet/imagenet_val.prototxt'
    blob_name = 'fc7'

use_gpu = False

# deep feature folder
deep_features_folder = features_folder + '/deep_features%s' % (postfix)

# tags number
if debug:
    tags_number = 2
else:
    tags_number = 144
resnet_batch = 50
extract_feature_batch = int(math.ceil(float(samples_per_category * tags_number) / float(resnet_batch)))
x_train_file = features_folder + '/x_train%s.pkl' % (postfix)
x_test_file = features_folder + '/x_test%s.pkl' % (postfix)
y_train_file = features_folder + '/y_train%s.pkl' % (postfix)
y_test_file = features_folder + '/y_test%s.pkl' % (postfix)
