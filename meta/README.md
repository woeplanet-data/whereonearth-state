states.csv
--

A vanilla CSV file mapping Natural Earth (NE) name, three-letter ISO code and
FIPS-1 code to Where On Earth ID. Note: _This is not a complete mapping_. It is
the result of geocoding the NE records using the Flickr API and limiting
possible results to only those places with (WOE) place type of 'state'.

See also: bin/geocode-naturalearth.py

states-has-woeid.csv
--

A subset of states.csv containing only those rows with a WOE ID.

states-needs-woeid.csv
--

A subset of states.csv containing rows without a WOE ID.
