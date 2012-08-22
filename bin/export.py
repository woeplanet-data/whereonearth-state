import sys
import json

fh = open(sys.argv[1], 'r')
data = json.load(fh)
fh.close()

count = len(data['features'])
print count

i = 0

while count > i:

    features = data['features'][i]
    id = features['properties'].get('woe:id', None)

    if id:

        path = "ne/%s.json" % id

        geojson = {
            'type': 'FeatureCollection',
            'features': [ features ]
            }
        
        fh = open(path, 'w')
        json.dump(geojson, fh)
        fh.close()

        print path

    i += 1


    
