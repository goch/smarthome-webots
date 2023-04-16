/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const label_motion_detected = document.querySelector("#motion_detected");

// A message coming from the robot has been received.
// new object message received
const onObjectMessage = (message) => {
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
    setMotionDetected(base.getStateValue('motion_detected'));  
}

function setMotionDetected(motion_detected){
    label_motion_detected.innerHTML = motion_detected.toString();
    if (motion_detected){
        label_motion_detected.style.background = "green";
    }else{
        label_motion_detected.style.background = "red";
    } 
}