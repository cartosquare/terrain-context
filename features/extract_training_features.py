import os
from config import caffe_model_file, caffe_proto_text, caffe_extract_features_bin, deep_features_folder, extract_feature_batch

if os.path.exists(deep_features_folder):
    os.mkdir(deep_features_folder)

# generate deep feature
cmd = '%s %s %s fc1000 %s %d leveldb' % (caffe_extract_features_bin, caffe_model_file, caffe_proto_text, deep_features_folder, extract_feature_batch)
os.system(cmd)
