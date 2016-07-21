import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import L18_image_list, L18_keys_file
import leveldb


db = leveldb.LevelDB(L18_keys_file)
with open(L18_image_list, 'r') as f:
    count = 0
    for line in f:
        file_path, x, y = line.strip().split()
        filename = x + '_' + y
        db.Put(filename, format(count, '010d'))
        count += 1
