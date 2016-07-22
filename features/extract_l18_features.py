import os
import shutil
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import caffe_model_file, caffe_proto_L18_text, caffe_extract_features_bin, L18_deep_features_folder, L18_extract_feature_batch, use_gpu, blob_name

# remove if exists
if os.path.exists(L18_deep_features_folder):
    shutil.rmtree(L18_deep_features_folder)

if use_gpu:
    db_type_str = 'GPU'
else:
    db_type_str = 'CPU'

print '#batch ', L18_extract_feature_batch

# generate deep feature
cmd = '%s %s %s %s %s %d leveldb db_type %s' % (caffe_extract_features_bin, caffe_model_file, caffe_proto_L18_text, blob_name, L18_deep_features_folder, L18_extract_feature_batch, db_type_str)
os.system(cmd)
