import os
import glob
import random
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import google_image_folder, image_list_txt, samples_per_category

f = open(image_list_txt, 'w')

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
        for idx in range(0, max_samples):
            f.write('%s %s\n' % (listing[idx], direc))
    else:
        print 'not directory: %s' % (label_directory)
f.close()
print '#class: %d, #samples: %d' % (class_count, samples_count)
