import datetime
import os
import json
import random
from config import train_dir, level

col_count = pow(2, level)

annotation = {}
annotation['info'] = {
    'year': 2016,
    'version': '1.0.0',
    'description': 'Building annotations of beijing urban',
    'contributor': 'XuXiang<xux@geohey.com>',
    'date_created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
annotation['licenses'] = [
    {
        'id': 3,
        'name': 'All rights reserved @Geohey',
        'url': 'http://cartosquare.com',
    }
]

annotation['images'] = []
annotation['annotations'] = []
annotation['categories'] = [{
    'id': 1,
    'name': 'building',
    'supercategory': 'manmade'
}]

annotation_val = {}
annotation_val['info'] = {
    'year': 2016,
    'version': '1.0.0',
    'description': 'Building annotations of beijing urban',
    'contributor': 'XuXiang<xux@geohey.com>',
    'date_created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
annotation_val['licenses'] = [
    {
        'id': 3,
        'name': 'All rights reserved @Geohey',
        'url': 'http://cartosquare.com',
    }
]

annotation_val['images'] = []
annotation_val['annotations'] = []
annotation_val['categories'] = [{
    'id': 1,
    'name': 'building',
    'supercategory': 'manmade'
}]

image_dir = os.path.join(train_dir, 'images')
anno_dir = os.path.join(train_dir, 'annotation')

# images
image_id = 0
image_list = os.listdir(image_dir)
total_count = len(image_list)
training_size = int(total_count * 0.7)
print '#images: ', total_count
print '#training: ', training_size

# random shuffle image list
random.shuffle(image_list)

# training image ids
train_image_id = []

# image id -> image path
image_map = {}

for image in image_list:
    image_file = os.path.join(image_dir, image)
    items = image.split('.')

    # make sure this is a png image
    if len(items) == 2 and items[1] == 'png':
        # fill image info
        image_obj = {
            'id': image_id,
            'width': 256,
            'height': 256,
            'file_name': image,
            'license': 3,
            'flickr_url': 'none',
            'coco_url': 'none',
            'date_captured': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # append to training/validating set according to image_id
        # 7/3 split of samples
        if image_id <= training_size:
            # training set
            annotation['images'].append(image_obj)
            train_image_id.append(image_id)
        else:
            # validating set
            annotation_val['images'].append(image_obj)

        image_map[image] = image_id
        image_id = image_id + 1

print 'training set #images: ', len(annotation['images'])
print 'validating set #images: ', len(annotation_val['images'])
print 'training image id set: ', len(train_image_id)

# annotations
anno_list = os.listdir(anno_dir)
anno_id = 0
for anno_name in anno_list:
    anno_file = os.path.join(anno_dir, anno_name)
    items = anno_name.split('.')
    # make sure this is a json file
    if len(items) == 2 and items[1] == 'json':
        # load json
        f = file(anno_file)
        s = json.load(f)
        f.close()

        # loop each annotation
        for anno in s['annotations']:
            # fill annotation info
            full_anno = anno
            full_anno['category_id'] = 1
            full_anno['id'] = anno_id
            full_anno['image_id'] = image_map[items[0] + '.png']
            full_anno['iscrowd'] = 0

            # skip empty annotation
            if len(anno['segmentation']) <= 0:
                continue

            segment = []
            for coordinate in anno['segmentation']:
                segment.append(coordinate[0])
                segment.append(coordinate[1])
            full_anno['segmentation'] = [segment]

            # append to training/validating set according to image_id
            if image_map[items[0] + '.png'] in train_image_id:
                annotation['annotations'].append(full_anno)
            else:
                annotation_val['annotations'].append(full_anno)

            anno_id = anno_id + 1

# saving ...
print 'saving %d training annotations' % len(annotation['annotations'])
with open('./train/instances_train2014.json', 'w') as trainfile:
    json.dump(annotation, trainfile)

print 'saving %d validating annotations' % len(annotation_val['annotations'])
with open('./train/instances_val2014.json', 'w') as valfile:
    json.dump(annotation_val, valfile)
