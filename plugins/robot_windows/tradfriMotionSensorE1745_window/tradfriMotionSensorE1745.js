/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_motion_detected = document.querySelector("#motion_detected");

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
    setMotionDetected(getStateValue('motion_detected'));  
}

function setMotionDetected(motion_detected){
    label_motion_detected.innerHTML = motion_detected.toString();
    if (motion_detected){
        label_motion_detected.style.background = "green";
    }else{
        label_motion_detected.style.background = "red";
    } 
}