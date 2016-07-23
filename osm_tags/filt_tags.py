"""
__file__

    config.py

__description__

    This filter subset tags from all_tags_csv file.

__author__

    atlasxu < xux@geohey.com >

"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import all_tags_csv, tags_csv, unique_tags_csv

# all_tags_csv file contains list all the tags
f1 = open(all_tags_csv, 'r')
# tags_csv contains the tags that we will use
f2 = open(tags_csv, 'w')
# unique_tags_csv contains all the tag names and index
f3 = open(unique_tags_csv, 'w')

lines = f1.readlines()
unique_labels = set()
labels_map = {}
first_line = True
for line in lines:
    if first_line:
        f2.write(line)
        first_line = False
    else:
        (tag, value, osm_type, label, label_cn, only_bj, use) = line.strip().split(',')
        if int(use):
            # only filter the tags that we indicate to use
            f2.write('%s,%s,%s,%s,%s,%s,%s\n' % (tag, value, osm_type, label, label_cn, only_bj, use))
            unique_labels.add(label)
            if label not in labels_map:
                labels_map[label] = label_cn

f1.close()
f2.close()

# print number of tags
print len(unique_labels)
print len(labels_map)

# sort tags and write to file
labels_list = sorted(unique_labels)
count = 0
for item in labels_list:
    f3.write('%s,%s,%d' % (item, labels_map[item], count))
    f3.write('\n')
    count += 1
f3.close()

print '#labels = %d' % (len(labels_list))
