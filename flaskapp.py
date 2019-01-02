#Metar Bug
#Patrick Pragman
#Ciego Services
#January 31, 2018
#Flask App to watch for changes in the weather

import json
from flask import Flask, render_template, request, Response, jsonify
from metar import Metar
from get_metar import get_metar

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_metar', methods=['POST'])
def get_report():
    req_data = request.form['code']

    try:
        raw_report = get_metar(req_data)
        if raw_report[0]:
            #if the report returns, build it and send it.
            obs = Metar.Metar(raw_report[1])

            lowest = 100000
            for skc in obs.sky:
                #find the lowest ceiling
                ht = int(skc[1].value())
                
                #a ceiling is the lowest broken or overcast layer
                if (skc[0] == "BKN" or skc[0] == "OVC"):
                    if ht < lowest:
                        lowest = skc[1].value()
                    
            response = {"ICAO": obs.station_id,
                        "RAW": obs.code,
                        "VIS": obs.vis.value(),
                        "CX": lowest,
                        "WIND": obs.wind_speed.value(),
                        "ERROR": False,
                        "ERROR_TYPE": "NA"}

            return jsonify(response)

        if not raw_report[0]:
            #if the report is unavailable, tell the user
            return jsonify({"ERROR" : True,
                        "ICAO" : req_data,
                        "ERROR_TYPE": raw_report[1]})
    except:
        #in the event that this process fails, we need to still send something back to the frontend
        #we'll call all of these "server errors" - at some point I should probably log these or something
        #I'm not sure what the best course of action for this would be.
        return jsonify({"ERROR" : True,
                        "ICAO" : req_data,
                        "ERROR_TYPE": "SERVER ERROR"})



@app.route('/get_stations',methods = ['GET'])
def get_stations():
    #open up the stations list and send it as requested
    path = "static/js/stations.json"
    with open(path, "r") as station_list:
        data = station_list.read()
        return data

if __name__ == "__main__":
    app.run()
