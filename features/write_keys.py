import sys
import os
import shutil

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import L18_image_list, L18_keys_file
import leveldb


def get_file_with_parents(filepath, levels=1):
    common = filepath
    for i in range(levels + 1):
        common = os.path.dirname(common)
    return os.path.relpath(filepath, common)

# remove if exists
if os.path.exists(L18_keys_file):
    shutil.rmtree(L18_keys_file)

db = leveldb.LevelDB(L18_keys_file)
with open(L18_image_list, 'r') as f:
    count = 0
    for line in f:
        file_path, label = line.strip().split()
        rel_path = get_file_with_parents(file_path, 1)
        y = str(rel_path).split('/')[0]

        base = os.path.basename(file_path)
        x = os.path.splitext(base)[0]

        filename = x + '_' + y
        db.Put(filename, format(count, '010d'))
        count += 1
        if count % 10000 == 0:
            print 'processed %d' % (count)
            print 'filename %s' % (filename)
