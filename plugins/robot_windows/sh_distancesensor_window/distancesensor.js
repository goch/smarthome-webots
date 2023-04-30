/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
console.log("Loading");
import * as base from "../_base/js/base.js"

const label_current_distance = document.querySelector("#currentDistance");
const input_trigger_distance = document.querySelector("#input_triggerDistance");
const label_triggered = document.querySelector("#label_triggered");
const btn_decrease_trigger = document.querySelector("#btn_decrease_trigger");
const btn_increase_trigger = document.querySelector("#btn_increase_trigger");

let trigger_distance = -1.0

btn_decrease_trigger.addEventListener('click', () => incrementTriggerDistance(-0.01));
btn_increase_trigger.addEventListener('click', () => incrementTriggerDistance(0.01));



// A message coming from the robot has been received.
// new object message received
const onObjectMessage = (message) => {
console.log("receivedObject")
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
    setDistance(base.getStateValue('distance'));
    setInputText(base.getStateValue('trigger_distance'));
    setTriggered(base.getStateValue('triggered'));
}

function setTriggered(triggered){
    label_triggered.innerHTML = triggered.toString();
    if (triggered){
        label_triggered.style.background = "green";
    }else{
        label_triggered.style.background = "red";
    } 
}

function setDistance(distance){
    label_current_distance.innerHTML = distance.toFixed(3) + " m";
}

function setInputText(value){
    trigger_distance = parseFloat(value)
    input_trigger_distance.value = trigger_distance.toFixed(3) + " m";
}

function incrementTriggerDistance(value){
    base.setStateValue('trigger_distance', parseFloat((trigger_distance + value).toFixed(3)));
    setInputText(trigger_distance + value);
}