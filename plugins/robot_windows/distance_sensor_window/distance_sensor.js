/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_current_distance = document.querySelector("#currentDistance");
const input_trigger_distance = document.querySelector("#input_triggerDistance");
const label_triggered = document.querySelector("#label_triggered");

let trigger_distance = -1.0

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
    setDistance(getStateValue('distance'));
    setInputText(getStateValue('trigger_distance'));
    setTriggered(getStateValue('triggered'));
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
    setStateValue('trigger_distance', parseFloat((trigger_distance + value).toFixed(3)));
    setInputText(trigger_distance + value);
}