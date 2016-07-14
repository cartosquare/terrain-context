import os
import shutil
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import caffe_model_file, caffe_proto_text, caffe_extract_features_bin, deep_features_folder, extract_feature_batch, use_gpu, blob_name

# remove if exists
if os.path.exists(deep_features_folder):
    shutil.rmtree(deep_features_folder)

if use_gpu:
    db_type_str = 'GPU'
else:
    db_type_str = 'CPU'

print '#batch ', extract_feature_batch

# generate deep feature
cmd = '%s %s %s %s %s %d leveldb db_type %s' % (caffe_extract_features_bin, caffe_model_file, caffe_proto_text, blob_name, deep_features_folder, extract_feature_batch, db_type_str)
os.system(cmd)
