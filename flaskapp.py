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
            obs = Metar.Metar(raw_report[1])

            lowest = 100000
            for skc in obs.sky:

                ht = int(skc[1].value())
                
                if (skc[0] == "BKN" or skc[0] == "OVC"):
                    if ht < lowest:
                        lowest = skc[1].value()
                    
            response = {"ICAO": obs.station_id,
                        "RAW": obs.code,
                        "VIS": obs.vis.value(),
                        "CX": lowest,
                        "WIND": obs.wind_speed.value()}

            return jsonify(response)
    except:
        print('Error')
        return jsonify({"Error" : "no data"})



@app.route('/get_stations',methods = ['GET'])
def get_stations():
    #open up the stations list and send it as requested
    path = "static/js/stations.json"
    with open(path, "r") as station_list:
        data = station_list.read()
        return data

if __name__ == "__main__":
    app.run()
