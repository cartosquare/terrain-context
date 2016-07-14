### This file contains all the configure parameters we need.

## general folders
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

# csv that combines node and way tags
all_tags_csv = osm_tags_folder + '/all_tags.csv'

# subset of all tags(This is the tags that we want to learn)
tags_csv = osm_tags_folder + '/tags.csv'

# in tags_csv file, a tag may occurs two times(both as node and way tags)
# in this file, we list all the unique tags
unique_tags_csv = osm_tags_folder + '/unique_tags.csv'

# extracted data by tags
tags_node_data_folder = osm_tags_folder + './tags_node_data'
tags_way_data_folder = osm_tags_folder + './tags_way_data'

# download list contains all the coordinates of corresponding tags
# in later works, we will download an image for each pair of coordinate
download_list_csv = osm_tags_folder + './download_list.csv'

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
google_image_folder = images_folder + '/google_images'


## features

# image list
image_list_txt = features_folder + '/image_list.txt'

# caffe binary
caffe_root = '../caffe/'
caffe_extract_features_bin = '../caffe/build/tools/extract_features.bin'
caffe_model_file = '../deep-residual-networks/ResNet-152-model.caffemodel'
caffe_proto_text = 'resnet/ResNet-152-deploy.prototxt'
use_gpu = True

# deep feature folder
deep_features_folder = features_folder + '/deep_features'
extract_feature_batch = samples_per_category
x_train_file = features_folder + '/x_train.pkl'
x_test_file = features_folder + '/x_test.pkl'
y_train_file = features_folder + '/y_train.pkl'
y_test_file = features_folder + '/x_train.pkl'
