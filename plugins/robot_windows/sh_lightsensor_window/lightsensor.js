/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_luminosity = document.querySelector("#label_luminosity");

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
    let luminosity = getStateValue('luminosity');
    if (!isNaN(luminosity)){
        setLuminosity(luminosity);
    }else
        setLuminosity(-1);
}

function setLuminosity(value){
    label_luminosity.innerHTML = value.toFixed(2) + " W/m²";
}