/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const label_currentTemp = document.querySelector("#label_currentTemp");
const input_setTemp = document.querySelector("#input_setTemp");
const button_reduceTemp = document.querySelector('#btn_reduceTemp');
const button_increaseTemp = document.querySelector('#btn_increaseTemp');

const label_currentHumidity = document.querySelector("#label_currentHumidity");
const input_setHumidity = document.querySelector("#input_setHumidity");
const button_reduceHumidity = document.querySelector('#btn_reduceHumidity');
const button_increaseHumidity = document.querySelector('#btn_increaseHumidity');


button_reduceHumidity.addEventListener('click', () => incrementSetHumidity(-1));
button_increaseHumidity.addEventListener('click', () => incrementSetHumidity(1))

button_reduceTemp.addEventListener('click', () => incrementSetTemp(-0.1));
button_increaseTemp.addEventListener('click', () => incrementSetTemp(0.1));

let currentTemp = null;
let setTemperature = null;

let currentHumidity = null;
let setHumidity = null;

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
    currentHumidity = base.getStateValue('currentHumidity');
    setHumidity = base.getStateValue('setHumidity');
    setCurrentTemp(currentTemp);
    setTemperatureText(setTemperature); 
    setCurrentHumidity(currentHumidity);
    setHumidityText(setHumidity);
}

input_setTemp.addEventListener ("change", function () {
    base.log("value input changed");
    let temp = parseFloat(this.value);
    setTemperatureText(this.value);
    base.setStateValue('setTemperature', temp);
});

input_setHumidity.addEventListener ("change", function () {
    base.log("value input changed");
    let humidity = parseFloat(this.value);
    setHumidityText(this.value);
    base.setStateValue('setTemperature', humidity);
});

function setCurrentTemp(value){
    label_currentTemp.innerHTML = value + "°C";
}

function setTemperatureText(value){
    input_setTemp.value = value + "°C";
}

function incrementSetTemp(value){
    base.setStateValue('setTemperature', parseFloat((setTemperature+value).toFixed(1)));
    setTemperatureText((setTemperature+value).toFixed(1));
}

function setCurrentHumidity(value){
    label_currentHumidity.innerHTML = value + "%";
}

function setHumidityText(value){
    input_setHumidity.value = value + "%";
}

function incrementSetHumidity(value){
    base.setStateValue('setHumidity', parseFloat((setHumidity+value).toFixed(1)));
    setHumidityText((setHumidity+value).toFixed(1));
}