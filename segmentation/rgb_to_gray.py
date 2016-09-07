from config import train_dir
import os
from skimage import color
from skimage import io

labels_3b_dir = train_dir + '/labels_3b'
label_dir = os.path.join(train_dir, 'labels')

image_list = os.listdir(labels_3b_dir)
for image in image_list:
    items = image.split('.')
    if len(items) == 2 and items[1] == 'png':
        image_path = os.path.join(labels_3b_dir, image)
        new_image_path = os.path.join(label_dir, image)
        print '%s -> %s' % (image_path, new_image_path)

        img = color.rgb2gray(io.imread(image_path))
        binary_img = img > 0
        binary_img = binary_img.astype(int)
        io.imsave(new_image_path, binary_img)
