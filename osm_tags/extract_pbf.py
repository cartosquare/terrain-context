import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import tags_csv, pbf_file, tags_node_data_folder, tags_way_data_folder, debug

if not os.path.exists(tags_node_data_folder):
    os.makedirs(tags_node_data_folder)

if not os.path.exists(tags_way_data_folder):
    os.makedirs(tags_way_data_folder)

with open(tags_csv) as f:
    count = 0
    first_line = True
    for line in f:
        # skip first line
        if first_line:
            first_line = False
            continue

        (key, val, osm_type, label, label_cn, only_bj, use) = line.strip().split(',')
        key_value = '%s.%s' % (key, val)

        if int(only_bj):
            spatial_filter = '--bounding-box top=41 left=115 bottom=39 right=117'
        else:
            spatial_filter = ''

        if osm_type == 'way':
            osm_tag_file = '%s/%s.osm' % (tags_way_data_folder, key_value)
            json_tag_file = '%s/%s.geojson' % (tags_way_data_folder, key_value)
            type_filter = '--tf accept-ways %s=%s --used-node' % (key, val)
        else:
            osm_tag_file = '%s/%s.osm' % (tags_node_data_folder, key_value)
            json_tag_file = '%s/%s.geojson' % (tags_node_data_folder, key_value)
            type_filter = '--node-key-value keyValueList="%s"' % (key_value)

        if debug:
            print tags_way_data_folder, tags_node_data_folder
            print osm_tag_file

        # generate if not exist
        if not os.path.exists(json_tag_file):
            extract_com = 'osmosis --read-pbf %s %s %s --write-xml %s' % (pbf_file, type_filter, spatial_filter, osm_tag_file)

            print extract_com
            os.system(extract_com)

            convert_com = 'osmtogeojson %s > %s' % (osm_tag_file, json_tag_file)
            print convert_com
            os.system(convert_com)
            # delete tem files, otherwise the disk usage will big!
            os.remove(osm_tag_file)
        else:
            print '%s already exist, skip' % (json_tag_file)
