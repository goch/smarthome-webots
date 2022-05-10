/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const label_current_distance = document.querySelector("#currentDistance");
const input_trigger_distance = document.querySelector("#input_triggerDistance");

let trigger_distance = -1.0

function setDistance(distance){
    label_current_distance.innerHTML = distance.toFixed(3) + " m";
}

function setInputText(value){
    trigger_distance = parseFloat(value)
    input_trigger_distance.value = trigger_distance.toFixed(3) + " m";
}

function incrementTriggerDistance(value){
    sendState('trigger_distance', parseFloat((trigger_distance + value).toFixed(3)));
    setInputText(trigger_distance + value);
}

// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            showStates(msg);
            label_device_name.innerHTML = msg['name'];
            setDistance(msg['data']["distance"]);
            setInputText(msg['data']["trigger_distance"])
        } catch (e) {}
    }
}