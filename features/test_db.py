import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import deep_features_folder, L18_keys_file
import leveldb


key_db = leveldb.LevelDB(L18_keys_file)
feature_db = leveldb.LevelDB(deep_features_folder)

print key_db.Get('2_3')
# print feature_db.Get('0000000000')
