"""
__file__

    config.py

__description__

    Download images from google.

__author__

    atlasxu < xux@geohey.com >

"""

import os
import random
from urllib2 import urlopen, URLError, HTTPError
from config import image_size, default_zoom, bottom_crop, samples_per_category, min_samples_per_category, KEY, download_list_csv, google_image_folder

if not os.path.exists(google_image_folder):
    os.makedirs(google_image_folder)


def dlfile(url, filename):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(filename, "wb") as local_file:
            local_file.write(f.read())

        # crop image
        command = 'mogrify -gravity north -extent %dx%d %s' % (image_size, image_size, filename)
        os.system(command)

    # handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

with open(download_list_csv) as f:
    count = 0
    finished = list()
    for line in f:
        (lon, lat, label) = line.strip().split(',')
        if label in finished:
            continue

        image_dir = '%s/%s' % (google_image_folder, label)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        old_files_num = len([name for name in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, name))])
        print 'already downloaded: ', old_files_num
        if old_files_num >= samples_per_category:
            finished.append(label)
            continue

        # download google image
        url_str = 'https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=%f,%f&zoom=%d&size=%dx%d&key=%s' % (float(lat), float(lon), default_zoom, image_size, image_size + bottom_crop, KEY)
        image_file = '%s/%s_%f_%f.png' % (image_dir, label, float(lon), float(lat))

        if not os.path.exists(image_file):
            print label
            dlfile(url_str, image_file)

            # delete invalid image
            if os.path.exists(image_file) and os.path.getsize(image_file) <= 2000:
                os.remove(image_file)
