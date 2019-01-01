//main.js
//This is the front end of Station Keeper
//Patrick Pragman
//Ciego Services
//January 31, 2018

//this is the div that contains the list of stations
//these globals (gross I know) control the page
var sld = document.getElementById('station_list_div');
var wld = document.getElementById('watch_list_div');
var sl = [];
var wl = [];
var time_interval = 1000*60*5; //default refresh interval is 5 minutes

//generic global function to GET json from the server
function getJSON(callback, target, payload=null, rtype="GET"){
    var xhr = new XMLHttpRequest;
    xhr.overrideMimeType("application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(JSON.parse(xhr.responseText));
        }
    };

    xhr.open(rtype,target,true);
    if (rtype == "POST"){
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }
    xhr.send(payload)
};

function load_stations(station_list){
    //load station list
    
    for (var i = 0; i< station_list.length; i++){

        sl.push(station_list[i])
    };

    populate_sld();
};

function populate_sld(){
    //populate the station_list_div

    sld.innerHTML = ""; //clear out the HTML in there

    for (var i = 0; i < sl.length; i++) {
        sld.appendChild(make_station(sl[i]));
    };

};

//makes a station div
function make_station(STA){

    var name = STA.NAME;
    var ICAO = STA.ICAO;
    var IATA = STA.IATA;

    var station = document.createElement("div")
    station.id = ICAO;
    station.innerText = name + " " + ICAO + " " + IATA;
    station.name = name + " " + ICAO + " " + IATA;
    station.onclick = function(){getJSON(watch,"get_metar","code=" + ICAO, rtype="POST")};
    station.style.display = "none";

    return station;

};


function watch(metar){
    //add a metar to the container
    //first we need to filter out 

    wl = wl.filter(report => report.ICAO != metar.ICAO);

    if (metar.Error != "no data"){
        var report = {
            "ICAO": metar.ICAO,
            "RAW" : metar.RAW,
            "CX" : metar.CX,
            "VIS": metar.VIS,
            "WIND": metar.WIND,
            "timer": setInterval(function(){getJSON(watch,"get_metar","code=" + metar.ICAO, rtype="POST");}, time_interval),
        }

        wl.push(report);

        populate_wld();
    };
}

function populate_wld(){
    //populate the watch_list_div

    wld.innerHTML = ""; //clear out the HTML in there

    for (var i = 0; i < wl.length; i++) {
        wld.appendChild(make_metar(wl[i]));
    };

}

function make_metar(RPT){
    //make a metar div

    var report = document.createElement("div")
    var name = RPT.NAME;
    var ICAO = RPT.ICAO;
    var RAW = RPT.RAW;
    var CX = RPT.CX;
    var VIS = RPT.VIS;
    var WIND = RPT.WIND;
    var TIME = RPT.TIME;
    var FLIGHT_RULES = "UNAVAILABLE";


    if (CX > 3000 && VIS > 5){
        FLIGHT_RULES = "VFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-success")

    }

    if (CX <= 3000 || VIS <= 5){
        FLIGHT_RULES = "MVFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-primary")

    }

    if (CX < 1000 || VIS <3){
        FLIGHT_RULES = "IFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-warning")

    }

    if (CX < 500 || VIS <= 2 ){
        FLIGHT_RULES = "LIFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-danger") 
    }
    
    report.id = ICAO + "_metar";
    report.innerText = "Flight Rules:  " + FLIGHT_RULES + "\n" + RAW;


    report.onclick = function(){
                                //get rid of the timer
                                clearInterval(RPT.timer);
                                //remove the object, then repopulate the list
                                wl = wl.filter(report => report.ICAO != ICAO);
                                populate_wld();
                            };


    return report;

};

function unhide(){
    //unhide stations on change
    
    var input = document.getElementById("search_box");
    var filter = input.value.toUpperCase();
    var div;
    station_list = sld.getElementsByTagName('div');

    // Loop through all list items, and hide those who don't match the search query

    for (var i = 0; i < station_list.length; i++) {
        div = station_list[i];
        if (div.innerText.toUpperCase().indexOf(filter) > -1) {
            div.style.display = "";
        } else {

            div.style.display = "none";}
    }

    if (filter == ""){
        for (var i = 0; i < station_list.length; i++){
            div = station_list[i];
            div.style.display = "none";
        }
    }
        
}

//first query the server for the station list
getJSON(load_stations,'get_stations');

