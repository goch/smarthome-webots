/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

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
base.register("object", onObjectMessage);
base.register("state", onStateMessage);
base.register("reset", onResetMessage);

//initialize WebUI
function init(){
  updateUI();
}

//update User Interface
function updateUI(){
    
}