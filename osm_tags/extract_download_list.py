import os
from random import randint
from osgeo import ogr
import json
import numpy as np
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import tags_csv, samples_per_category, min_samples_per_category, lng_offset, lat_offset, tags_node_data_folder, tags_way_data_folder, download_list_csv, debug

with open(tags_csv) as f:
    count = 0
    first_line = True
    coordinates_map = {}

    for line in f:
        # skip first line
        if first_line:
            first_line = False
            continue

        (key, val, osm_type, label, label_cn, only_bj, use) = line.strip().split(',')
        key_value = '%s.%s' % (key, val)

        if osm_type == 'way':
            json_file = '%s/%s.geojson' % (tags_way_data_folder, key_value)
        elif osm_type == 'node':
            json_file = '%s/%s.geojson' % (tags_node_data_folder, key_value)
        else:
            print 'Invalid osm type', osm_type
            continue

        print key_value
        if not os.path.exists(json_file):
            print key_value, 'not exist'
            continue

        if label not in coordinates_map:
            coordinates_map[label] = []

        with open(json_file) as ff:
            data = json.load(ff)
            total_features = len(data['features'])

            for feature in data['features']:
                if len(coordinates_map[label]) >= samples_per_category:
                    break

                if osm_type == 'way':
                    # if debug:
                    #    print 'process way'
                    if (feature['geometry']['type'] == 'Point' or 'properties' not in feature or key not in feature['properties'] or feature['properties'][key] != val):
                        continue

                    if feature['geometry']['type'] == 'Polygon':
                        rings = feature['geometry']['coordinates']
                        coord_len = len(rings[0])
                        # if debug:
                        #    print '\tprocess polygon'
                        if total_features > samples_per_category:
                            # if debug:
                            #    print '\trandom select a vertice'
                            coordinates_map[label].append(rings[0][randint(0, coord_len - 1)])
                        else:
                            # if debug:
                            #    print 'discrect polygon ...'
                            geojson = json.dumps(feature['geometry'])
                            # print geojson

                            geom = ogr.CreateGeometryFromJson(geojson)
                            env = geom.GetEnvelope()
                            # longitude range
                            for x in np.arange(env[0], env[1], lng_offset):
                                # latitude range
                                for y in np.arange(env[2], env[3], lat_offset):
                                    point = ogr.Geometry(ogr.wkbPoint)
                                    point.AddPoint(x, y)
                                    # print point
                                    intersection_pt = geom.Intersection(point)
                                    if not intersection_pt.IsEmpty():
                                        coordinates_map[label].append([x, y])

                    elif feature['geometry']['type'] == 'LineString':
                        # if debug:
                        #   print '\tprocess linestring'
                        line = feature['geometry']['coordinates']
                        if total_features > samples_per_category:
                            # if debug:
                            #    print '\trandom select a vertice'
                            coordinates_map[label].append(line[randint(0, len(line) - 1)])
                        else:
                            # if debug:
                            #    print 'discrect linestring ...'
                            last_lng = line[0][0]
                            last_lat = line[0][1]
                            for idx in range(1, len(line)):
                                if (abs(line[idx][0] - last_lng) > lng_offset or abs(line[idx][1] - last_lat) > lat_offset):
                                    last_lng = line[idx][0]
                                    last_lat = line[idx][1]
                                    coordinates_map[label].append([last_lng, last_lat])
                    elif feature['geometry']['type'] == 'MultiPolygon':
                        print 'mulitpolygon...'
                    elif feature['geometry']['type'] == 'MultiLineString':
                        print 'multiLineString...'
                    else:
                        print 'unknow geometry type: ', feature['geometry']['type']
                elif osm_type == 'node':
                    # if debug:
                    #    print 'process node'
                    # NEED TO CHECK THIS LINE!
                    coordinates_map[label].append(feature['geometry']['coordinates'])
                else:
                    print 'Invalid osm type', osm_type

    # save all the coordinate pair
    csv_handle = open(download_list_csv, 'w')
    for tag in coordinates_map:
        coordinates = coordinates_map[tag]
        print 'label %s has %d samples' % (tag, len(coordinates_map[tag]))
        for coord in coordinates:
            csv_handle.write('%.7f,%.7f,%s\n' % (coord[0], coord[1], tag))
    csv_handle.close()
