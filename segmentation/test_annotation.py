from pycocotools.coco import COCO
import numpy as np
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

dataDir='/Volumes/first/ml/ml/terrain-context/segmentation/train'
annFile='%s/building_annotations.json'%(dataDir)

coco=COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print 'COCO categories: \n\n', ' '.join(nms)

nms = set([cat['supercategory'] for cat in cats])
print 'COCO supercategories: \n', ' '.join(nms)

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['building']);
imgIds = coco.getImgIds(catIds=catIds );
random_img = imgIds[np.random.randint(0,len(imgIds))]
#img = coco.loadImgs()[0]
print random_img

annIds = coco.getAnnIds(imgIds=random_img, catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
print len(anns)
