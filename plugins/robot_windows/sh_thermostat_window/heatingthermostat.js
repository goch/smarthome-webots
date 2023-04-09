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
const object_msg = function on_ObjectMessage(message){
    initUI();
}
  

// new state message received
const onStateMessage = function on_StateMessage(message){
    updateUI();
}
// new reset message received
const onResetMessage = function on_ResetMessage(message){

}

base.register_OnObjectMessage(object_msg);
base.register_OnStateMessage(onStateMessage);
base.register_OnResetMessage(onResetMessage);

//setup User Interface
function initUI(){

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
    base.setStateValue('setTemperature', parseFloat((setTemperature+value).toFixed(1)));
    setInputText((setTemperature+value).toFixed(1));
}



