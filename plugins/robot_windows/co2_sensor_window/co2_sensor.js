/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_air_quality = document.querySelector("#label_airQuality");
const label_co2_concentration = document.querySelector("#label_CO2Concentration");

// A message coming from the robot has been received.
// new object message received
function on_ObjectMessage(message){
    initUI();
}
  // new state message received
  function on_StateMessage(message){
    updateUI();
  }
  // new reset message received
  function on_ResetMessage(message){
  
  }

//setup User Interface
function initUI(){
    
    updateUI();
}
//update User Interface
function updateUI(){
    setAirQuality(getStateValue('air_quality'));
    setCO2Concentration(getStateValue('co2_concentration'));    
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