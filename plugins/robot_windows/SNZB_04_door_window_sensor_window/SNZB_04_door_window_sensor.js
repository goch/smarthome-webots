/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"


const label_triggered = document.querySelector("#label_triggered");


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
    setTriggered(base.getStateValue('contact'));
}

function setTriggered(triggered){
    label_triggered.innerHTML = triggered.toString();
    if (triggered){
        label_triggered.style.background = "green";
    }else{
        label_triggered.style.background = "red";
    } 
}





