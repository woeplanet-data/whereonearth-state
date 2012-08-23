#!/usr/bin/env python

import sys
import json
import Flickr.API
import csv
import pprint

apikey = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

api = Flickr.API.API(apikey)

fh = open(infile, 'r')
data = json.load(fh)
fh.close()

out = open(outfile, 'w')
writer = csv.writer(out)
writer.writerow(('name', 'iso', 'fips', 'woeid'))

count = len(data['features'])

i = 0

while count > i:

    props = data['features'][i]['properties']

    country = props.get('NAME_0', '')
    region = props.get('NAME_1', '')
    iso = props.get('ISO', '')
    fips = props.get('FIPS_1', '')

    if not country or country == '':
        country = iso

    if not fips or fips == '':
        n = "%s %s" % (region, country)
    else:
        n = "%s (%s) %s" % (region, fips, country)

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
        print "[OK] %s: %s" % (n.encode("ascii", "ignore"), woeid)

    else:
        print "[FAIL] %s" % n

    if region:
        region = region.encode('utf8')

    writer.writerow((region, iso, fips, woeid))

    i += 1
