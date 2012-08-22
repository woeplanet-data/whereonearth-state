import sys
import json
import Flickr.API
import pprint

key = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

api = Flickr.API.API(key)

fh = open(infile, 'r')
data = json.load(fh)
fh.close()

count = len(data['features'])
print count

i = 0

while count > i:

    region = data['features'][i]['properties'].get('NAME_1', '')
    iso = data['features'][i]['properties'].get('ISO', '')

    n = "%s, %s" % (region, iso)

    query = n.encode('utf8')

    req = Flickr.API.Request(method='flickr.places.find', query=query, format='json', nojsoncallback=1, sign=False)
    rsp = api.execute_request(req)

    fl_data = json.load(rsp)
    woeid = None

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

    i += 1

fh = open(outfile, 'w')
json.dump(data, fh)
fh.close()
