import os
import time
import sys

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print "Need Parameters, list below IN ORDER: "
        print "1th parameter: Directory which will contains the generated tiles"
        print "2th parameter: which level to process"
        print "3th parameter: min x coordinate"
        print "4th parameter: min y coordinate"
        print "5th parameter: max x coordinate"
        print "6th parameter: max y coordidate"
        exit(0)

    # Following parameters will be passed in
    out = sys.argv[1]
    print "out: ", out

    # zoom level
    level = int(sys.argv[2])
    print "level:", level

    # tile extent
    minx = float(sys.argv[3])
    miny = float(sys.argv[4])
    maxx = float(sys.argv[5])
    maxy = float(sys.argv[6])
    print minx, miny, maxx, maxy

    # mercator parameters
    worldOriginalx = -20037508.342787
    worldOriginaly = 20037508.342787

    # tile size
    tileSize = 256

    # resolutions for each level
    zoomReses = [156543.033928, 78271.516964, 39135.758482, 19567.879241, 9783.9396205, 4891.96981025, 2445.984905125,
                 1222.9924525625, 611.49622628125, 305.748113140625, 152.8740565703125, 76.43702828515625, 38.21851414257813,
                 19.10925707128906, 9.55462853564453, 4.777314267822266, 2.388657133911133, 1.194328566955567, 0.597164283477783, 0.298582141738892, 0.14929107086945, 0.07464553543473]

    tileExtent = tileSize * zoomReses[level]
    minBundlex = int((minx - worldOriginalx) / tileExtent)
    minBundley = int((worldOriginaly - maxy) / tileExtent)

    maxBundlex = int((maxx - worldOriginalx) / tileExtent)
    maxBundley = int((worldOriginaly - miny) / tileExtent)

    totalBundles = (maxBundlex - minBundlex + 1) * \
        (maxBundley - minBundley + 1)
    print "[Normal] total tiles #%s" % totalBundles

    step = totalBundles / 50 + 1
    count = 0
    status = 0
    maxIdx = 2 ** level - 1
    print "Max Idx: ", maxIdx

    for i in range(minBundlex, maxBundlex + 1):
        if i > maxIdx:
            continue
        for j in range(minBundley, maxBundley + 1):
            if j > maxIdx:
                continue

            tilepath = os.path.join(out, "%s" % (
                str(level) + "_" + str(i) + "_" + str(j) + ".png"))

            if not os.path.exists(tilepath):
                command = "curl 'http://khm1.googleapis.com/kh?v=691&&x=%d&y=%d&z=%d' -o %s" % (i, j, level, tilepath)
                print command
                print 'processed %f of %d' % (status, totalBundles)
                os.system(command)

            if os.path.exists(tilepath) and os.path.getsize(tilepath) < 1024:
                os.remove(tilepath)
                time.sleep(5)

            count += 1
            # process bar
            if (count % step == 0):
                status = (count / float(totalBundles) * 100)
                print "[Normal]level %s current processed: %.2f%%" % (str(level), status)
