#!/usr/bin/env python3 

import sys
import json

with open(sys.argv[1]) as f:
  data = json.load(f)


print("Number of features before filtering: " + str(len(data['features'])))

for i in list(data['features']):	
	if i['properties']['RoadUse'] == 'Private':
		data['features'].remove(i) 
	
print("Number of features after filtering: " + str(len(data['features'])))


newfile = sys.argv[1].replace(".geojson","")+"_no_privates.geojson"

with open(newfile, 'w') as json_file: 
  json_file.write(json.dumps(data, indent=3))
  json_file.close()
