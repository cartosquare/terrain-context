from config import all_tags_csv

with open(all_tags_csv) as f:
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            print line
            (tag, value, osm_type, label, label_cn, only_bj, use) = line.strip().split(',')
            # print label
            (prefix, postfix) = label.split('-')
            if prefix not in ('poi', 'way', 'landuse'):
                print 'Invalid label preix: ', label
            if postfix != value:
                print 'Invalid label postfix: ', label
