/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const label_currentTemp = document.querySelector("#label_currentTemp");
const input_setTemp = document.querySelector("#input_setTemp");

let currentTemp = null;
let setTemperature = null;

input_setTemp.addEventListener ("change", function () {
    log("value input changed");
    let temp = parseFloat(this.value);
    setInputText(this.value);
    sendState('setTemperature', temp);
});

function setInputText(value){
    input_setTemp.value = value + "°C";
}

function incrementSetTemp(value){
    sendState('setTemperature', parseFloat((setTemperature+value).toFixed(1)));
    setInputText((setTemperature+value).toFixed(1));
}
  
// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            label_device_name.innerHTML = msg['name'];
            showStates(msg);
            currentTemp = msg["data"]["currentTemperature"];
            setTemperature = msg["data"]["setTemperature"];
            label_currentTemp.innerHTML = currentTemp + "°C";
            setInputText(setTemperature); 
            setSlider(setTemperature);
        } catch (e) {}
    }
}