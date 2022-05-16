/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_currentTemp = document.querySelector("#label_currentTemp");
const input_setTemp = document.querySelector("#input_setTemp");

let currentTemp = null;
let setTemperature = null;

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
    currentTemp = getStateValue('currentTemperature');
    setTemperature = getStateValue('setTemperature');
    setCurrentTemp(currentTemp);
    setInputText(setTemperature); 
}


input_setTemp.addEventListener ("change", function () {
    log("value input changed");
    let temp = parseFloat(this.value);
    setInputText(this.value);
    setStateValue('setTemperature', temp);
});

function setCurrentTemp(value){
    label_currentTemp.innerHTML = value + "°C";
}


function setInputText(value){
    input_setTemp.value = value + "°C";
}

function incrementSetTemp(value){
    setStateValue('setTemperature', parseFloat((setTemperature+value).toFixed(1)));
    setInputText((setTemperature+value).toFixed(1));
}