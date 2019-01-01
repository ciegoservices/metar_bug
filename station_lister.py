#Station Maker
#Patrick Pragman
#Ciego Services
#January 31, 2018

#This script builds a list of all the METAR stations from https://www.aviationweather.gov/docs/metar/stations.txt in JSON.
#I downloaded the station list on January 31st, 2018 then manually deleted down to the start of the stations.

from json import dumps

with open('stations.txt',"r") as stations:
    with open('stations.json', 'w') as data:
        #open a file to write all the JSON into
        station_list = []

        for line in stations:

                #convert binary to str
                if not isinstance(line, str):
                    #convert from Bytes to str
                    line = line.decode()

            
                if not len(line.split()) < 8:
                    if not line.split()[0] == "CD":
                        #we've cut out most of the chaff
                        #now time to make some JSON objects
                        #here is a typical station string
                        #QC FRELIGHSBURG     CWFQ  WFQ   71373  45 02N  072 49W  152   X                7 CA


                        province = line[0:2].strip()
                        station_name = line[3:20].strip()
                        ICAO_ID = line[20:25].strip()
                        IATA = line[26:31].strip()
                        LAT = line[39:45].strip()
                        LON = line[47:55].strip()
                        ELV = line[54:62].strip()

                        station = {"NAME" : station_name,
                                    "ICAO" : ICAO_ID,
                                    "IATA" : IATA,
                                    "LAT" : LAT,
                                    "LON" : LON,
                                    "ELEV": ELV
                        }

                        station_list.append(station)
        #now we can write the JSON to a file

        json_data = dumps(station_list, sort_keys = True, indent = 4)
        data.write(json_data) #write it to a file




