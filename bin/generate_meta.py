#!/usr/bin/env python

import sys
import json
import os
import csv

import pprint
import utils

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])
    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    datadir = os.path.join(rootdir, 'data')
    metadir = os.path.join(rootdir, 'meta')

    # generate a list of all the states - assume the extractotron cities.txt
    # https://github.com/migurski/Extractotron/blob/master/cities.txt

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)

            fh = open(path)
            data = json.load(fh)

            feature = data['features'][0]
            props = feature['properties']

            this_woeid = props.get('woe:id', False)

            if not this_woeid:
                this_woeid = props.get('woeid', False)

            if not this_woeid:
                print pprint.pformat(props)
                sys.exit()

            try:
                centroid = [ props['longitude'], props['latitude'] ]
            except Exception, e:
                logging.error("failed to process %s: %s" % (path, e))
                # wtf?
                continue

            add_country = True

            for pt in ('sw_latitude', 'sw_longitude', 'ne_latitude', 'ne_longitude'):
                if not props.get(pt, False):
                    add_country = False
                    break

            if add_country:

                states_path = os.path.join(metadir, 'states-%s.tsv' % props['iso'])

                if os.path.exists(states_path):
                    states_fh = open(states_path, 'a')
                    states_writer = csv.writer(states_fh, delimiter='\t')
                else:
                    states_fh = open(states_path, 'w')
                    states_writer = csv.writer(states_fh, delimiter='\t')
                    states_writer.writerow(('top', 'left', 'bottom', 'right', 'slug', 'name', 'iso', 'woeid'))

                states_writer.writerow((
                        props['ne_latitude'],
                        props['sw_longitude'],
                        props['sw_latitude'],
                        props['ne_longitude'],
                        this_woeid,
                        props['name'].encode('utf-8'),
                        props['iso'],
                        this_woeid
                        ))

                states_fh.close()
