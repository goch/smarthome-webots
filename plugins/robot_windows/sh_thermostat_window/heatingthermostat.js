/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const label_currentTemp = document.querySelector("#label_currentTemp");
const input_setTemp = document.querySelector("#input_setTemp");
const button_reduceTemp = document.querySelector('#btn_reduceTemp');
const button_increaseTemp = document.querySelector('#btn_increaseTemp');

button_reduceTemp.addEventListener('click', () => incrementSetTemp(-0.1));
button_increaseTemp.addEventListener('click', () => incrementSetTemp(0.1));

let currentTemp = null;
let setTemperature = null;

// A message coming from the robot has been received.
// new object message received
const onObjectMessage = (message) => {
    init();
};
  
// new state message received
const onStateMessage = (message) => {
    updateUI();
};
// new reset message received
const onResetMessage = (message) => {

};
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
    currentTemp = base.getStateValue('currentTemperature');
    setTemperature = base.getStateValue('setTemperature');
    setCurrentTemp(currentTemp);
    setInputText(setTemperature); 
}

input_setTemp.addEventListener ("change", function () {
    base.log("value input changed");
    let temp = parseFloat(this.value);
    setInputText(this.value);
    base.setStateValue('setTemperature', temp);
});

function setCurrentTemp(value){
    label_currentTemp.innerHTML = value + "°C";
}

function setInputText(value){
    input_setTemp.value = value + "°C";
}

function incrementSetTemp(value){
    base.setStateValue('setTemperature', parseFloat((setTemperature+value).toFixed(1)));
    setInputText((setTemperature+value).toFixed(1));
}