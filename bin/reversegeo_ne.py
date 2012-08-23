#!/usr/bin/env python

import sys
import json
import Flickr.API
import csv
import pprint

key = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

api = Flickr.API.API(key)

fh = open(infile, 'r')
data = json.load(fh)
fh.close()

out = open(outfile, 'w')
writer = csv.writer(out)
writer.writerow(('iso', 'fips', 'woeid'))

count = len(data['features'])

i = 0

while count > i:

    props = data['features'][i]['properties']

    region = props.get('NAME_1', '')
    iso = props.get('ISO', '')
    fips = props.get('FIPS_1', '')

    # print pprint.pformat(props)
    # sys.exit()

    n = "%s, %s" % (region, iso)

    query = n.encode('utf8')

    req = Flickr.API.Request(method='flickr.places.find', query=query, format='json', nojsoncallback=1, sign=False)
    rsp = api.execute_request(req)

    fl_data = json.load(rsp)
    woeid = 0

    for pl in fl_data['places']['place']:

        if pl['place_type'] != 'region':
            continue

        woeid = pl['woeid']
        break

    if woeid:
        print "%s: %s" % (n.encode("ascii", "ignore"), woeid)
        data['features'][i]['properties']['woe:id'] = woeid

    else:

        print "FAILED: %s" % n
        # print pprint.pformat(fl_data)
        # print pprint.pformat(data['features'][i]['properties'])
        # sys.exit()

    writer.writerow((iso, fips, woeid))

    i += 1
