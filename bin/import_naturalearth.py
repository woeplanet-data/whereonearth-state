#!/usr/bin/env python

import sys
import os
import csv

import utils

import json
import shapely.geometry

import pprint

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    nepath = os.path.abspath(sys.argv[1])	# NE source files
    states = os.path.abspath(sys.argv[2])	# map of NE keys -> WOE ID

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    datadir = os.path.join(rootdir, 'data')
    metadir = os.path.join(rootdir, 'meta')

    reader = csv.reader(open(states, 'U'))
    lookup = {}

    for row in reader:
        label = "%s %s %s" % (row[0], row[1], row[2])
        woeid = row[3]

        lookup[label] = woeid

    nefh = open(nepath, 'r')
    nedata = json.load(nefh)

    for f in nedata['features']:

        props = f['properties']

        name = props.get('NAME_1', '')
        fips = props.get('FIPS_1', '')
        iso = props.get('ISO', '')

        label = "%s %s %s" % (name, iso, fips)
        woeid = lookup.get(label, 0)

        print "label: %s -> %s" % (label, woeid)

        if not woeid:
            continue

        root = utils.woeid2path(woeid)
        fname = '%s.json' % woeid

        woe_root = os.path.join(root, fname)
        woe_path = os.path.join(datadir, woe_root)

        if not os.path.exists(woe_path):
            continue

        print "%s: %s" % (iso, woe_path)

        geom = f['geometry']

        shp = shapely.geometry.asShape(geom)
        bbox = shp.bounds

        woe_fh = open(woe_path, 'r')
        woe_data = json.load(woe_fh)
        woe_fh.close()

        features = woe_data['features'][0]

        features['geometry'] = geom

        features['properties']['sw_longitude'] = bbox[0]
        features['properties']['sw_latitude'] = bbox[1]
        features['properties']['ne_longitude'] = bbox[2]
        features['properties']['ne_latitude'] = bbox[3]

        for k, v in props.items():
            k = "ne:%s" % k

            if k == 'ne:woe:id':
                continue

            features['properties'][k] = v

        to_delete = ('woeid', 'ne:woe:id')
        
        for k in to_delete:
        
            if features['properties'].has_key(k):
                del(features['properties'][k])

        features['properties']['woe:id'] = woeid  

        woe_data['bbox'] = bbox
        woe_data['features'] = [ features ]

        woe_fh = open(woe_path, 'w')
        json.dump(woe_data, woe_fh, indent=2)
        woe_fh.close()

    print "- done -"
    sys.exit()

