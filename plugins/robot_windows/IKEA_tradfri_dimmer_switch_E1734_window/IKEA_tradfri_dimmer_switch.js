/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const console_element = document.querySelector("#console");

let pressed_long = false;
let long_pressed_duration = 500;
let timeout = null;


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


function on_MouseDown(button){
  
timeout = setTimeout (() =>{
    log(button +" pressed long");
    pressed_long = true
    setStateValue(button,true);
  },long_pressed_duration);
}

function on_MouseUp(button){
  clearTimeout(timeout)

  // button pressed long
  if (pressed_long){
    pressed_long = false;
    setStateValue(button,false);
  }
  // button pressed short
  else{
    log(button + " pressed short");
    if (button == 'up_button')
      setStateValue('state',true);
    else{
      setStateValue('state',false)
    }
    
  }
}