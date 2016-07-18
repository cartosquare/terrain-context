import os
import glob
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import L18_image_folder, L18_image_list

f = open(L18_image_list, 'w')
subdirectories = os.listdir(L18_image_folder)
samples_count = 0
for direc in subdirectories:
    print direc
    label_directory = os.path.join(L18_image_folder, direc)
    if os.path.isdir(label_directory):
        listing = glob.glob(label_directory + '/*.png')

        for file in listing:
            if os.path.getsize(file) > 1024:
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]
                print filename
                f.write('%s %s %s\n' % (file, direc, filename))
            else:
                print 'skip invalid image %s' % (file)
    else:
        print 'not directory: %s' % (label_directory)
f.close()
