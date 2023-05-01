/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

//const label_device_name = document.querySelector("#device_name");

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
//register callbacks for incoming messages
base.subscribe("object", onObjectMessage);
base.subscribe("state", onStateMessage);
base.subscribe("reset", onResetMessage);

//initialize WebUI
function init(){
  updateUI();
}

//update User Interface
function updateUI(){
    
}