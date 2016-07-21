import sys
import os
import shutil

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import L18_image_list, L18_keys_file
import leveldb

# remove if exists
if os.path.exists(L18_keys_file):
    shutil.rmtree(L18_keys_file)

db = leveldb.LevelDB(L18_keys_file)
with open(L18_image_list, 'r') as f:
    count = 0
    for line in f:
        file_path, x, y = line.strip().split()
        # Warning: in the L18 image list file, the position of x and y are switched.
        filename = y + '_' + x
        db.Put(filename, format(count, '010d'))
        count += 1
        if count % 10000 == 0:
            print 'processed %d' % (count)
