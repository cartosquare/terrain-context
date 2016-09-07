from config import tile_dir, train_dir, tile_list_file, level
import os
import shutil

image_dir = os.path.join(train_dir, 'images')
label_dir = os.path.join(train_dir, 'labels')

if not os.path.exists(image_dir):
    os.makedirs(image_dir)
if not os.path.exists(label_dir):
    os.makedirs(label_dir)

f = open(tile_list_file, 'w')

x_list = os.listdir(tile_dir)
for x in x_list:
    x_path = os.path.join(tile_dir, x)
    if os.path.isdir(x_path):
        y_list = os.listdir(x_path)

        for y_file in y_list:
            items = y_file.split('.')
            if len(items) == 2 and items[1] == 'png':
                y = items[0]
                y_path = os.path.join(x_path, y_file)

                # record this tile
                f.write('%s/%s/%s\n' % (level, x, y))

                # copy to destination
                dest_path = os.path.join(image_dir, '%s_%s_%s' % (level, x, y_file))

                print '%s -> %s' % (y_path, dest_path)

                shutil.copyfile(y_path, dest_path)
f.close()
