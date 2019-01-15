#filter all the stations out with no ICAO code


import json

with open("stations.json", "r") as stations:
    jdata = json.loads(stations.read())

new_jdata = []

for entry in jdata:
    if entry['ICAO'] is not "":
        new_jdata.append(entry)

stations.close()

with open("stations.json", "w") as stations:
    stations.write(json.dumps(new_jdata, sort_keys = True, indent = 4))
