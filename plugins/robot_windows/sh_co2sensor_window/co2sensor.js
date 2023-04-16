/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const label_air_quality = document.querySelector("#label_airQuality");
const label_co2_concentration = document.querySelector("#label_CO2Concentration");

// A message coming from the robot has been received.
// new object message received
const onObjectMessage = (message) => {
    init();
  }
  // new state message received
  const onStateMessage = (message) => {
    updateUI();
  }
  // new reset message received
  const onResetMessage = (message) => {
  
  }
//subscribe to incoming messages
base.subscribe("object", onObjectMessage);
base.subscribe("state", onStateMessage);
base.subscribe("reset", onResetMessage);

//initialize WebUI
function init(){
  updateUI();
}

//update User Interface
function updateUI(){
    setAirQuality(base.getStateValue('air_quality'));
    setCO2Concentration(base.getStateValue('co2_concentration'));    
}

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