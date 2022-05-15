/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const label_air_quality = document.querySelector("#label_airQuality");
const label_co2_concentration = document.querySelector("#label_CO2Concentration");


function setCO2Concentration(value){
    label_co2_concentration.innerHTML = value + " ppm";
}

function setAirQuality(quality){
    
    label_air_quality.innerHTML = quality;
    switch (quality) {
        case "GOOD":
            label_air_quality.style.background = "green";
            break;
        case "BAD":
            label_air_quality.style.background = "orange";
            break;
        case "CRITICAL":
            label_air_quality.style.background = "red";
            break;
    
    
        default:
            label_air_quality.style.background = "grey";
            break;
    }
    
    
}


// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            showStates(msg);
            label_device_name.innerHTML = msg['name'];
            setAirQuality(msg["data"]['air_quality']);
            setCO2Concentration(msg["data"]['co2_concentration']);
        } catch (e) {}
    }
}

