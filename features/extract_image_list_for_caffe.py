"""
__file__

    config.py

__description__

    Get image list.

__author__

    atlasxu < xux@geohey.com >

"""

import os
import glob
import random
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import google_image_folder, train_image_list_txt, test_image_list_txt, samples_per_category, unique_tags_csv

f1 = open(train_image_list_txt, 'w')
f2 = open(test_image_list_txt, 'w')

tags_map = {}
with open(unique_tags_csv, 'r') as ff:
    for line in ff:
        (tag, tag_cn, label) = line.strip().split(',')
        tags_map[tag] = label

subdirectories = os.listdir(google_image_folder)
class_count = 0
samples_count = 0
for direc in subdirectories:
    label_directory = os.path.join(google_image_folder, direc)
    if os.path.isdir(label_directory):
        class_count += 1

        listing = glob.glob(label_directory + '/*.png')
        random.shuffle(listing)

        max_samples = samples_per_category
        if max_samples > len(listing):
            max_samples = len(listing)

        samples_count += max_samples

        cutline = int(max_samples * 0.6)

        # write training samples
        for idx in range(0, cutline):
            if os.path.getsize(listing[idx]) > 1024:
                f1.write('%s %s\n' % (listing[idx], tags_map[direc]))
            else:
                print 'skip training invalid image %s' % (listing[idx])

        # write testing samples
        for idx in range(cutline, max_samples):
            if os.path.getsize(listing[idx]) > 1024:
                f2.write('%s %s\n' % (listing[idx], tags_map[direc]))
            else:
                print 'skip testing invalid image %s' % (listing[idx])
    else:
        print 'not directory: %s' % (label_directory)

f1.close()
f2.close()
print '#class: %d, #samples: %d' % (class_count, samples_count)
