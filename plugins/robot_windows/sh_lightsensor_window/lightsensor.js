/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"


const label_luminosity = document.querySelector("#label_luminosity");

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
    let luminosity = base.getStateValue('luminosity');
    if (!isNaN(luminosity)){
        setLuminosity(luminosity);
    }else
        setLuminosity(-1);
}

function setLuminosity(value){
    label_luminosity.innerHTML = value.toFixed(2) + " W/m²";
}