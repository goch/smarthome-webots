/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const console_element = document.querySelector("#console");

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
    
}