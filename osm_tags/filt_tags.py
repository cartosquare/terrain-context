import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import all_tags_csv, tags_csv, unique_tags_csv

f1 = open(all_tags_csv, 'r')
f2 = open(tags_csv, 'w')
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
            f2.write('%s,%s,%s,%s,%s,%s,%s\n' % (tag, value, osm_type, label, label_cn, only_bj, use))
            unique_labels.add(label)
            if label not in labels_map:
                labels_map[label] = label_cn

f1.close()
f2.close()

print len(unique_labels)
print len(labels_map)

labels_list = sorted(unique_labels)
count = 0
for item in labels_list:
    f3.write('%s,%s,%d' % (item, labels_map[item], count))
    f3.write('\n')
    count += 1
f3.close()

print '#labels = %d' % (len(labels_list))
