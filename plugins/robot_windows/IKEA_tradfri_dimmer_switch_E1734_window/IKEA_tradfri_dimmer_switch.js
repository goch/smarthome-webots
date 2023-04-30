/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const console_element = document.querySelector("#console");
const btn_on = document.querySelector("#btn_on");
const btn_off = document.querySelector("#btn_off");


let pressed_long = false;
let long_pressed_duration = 500;
let timeout = null;


btn_on.onmousedown = (event) => {on_MouseDown('up_button')};
btn_on.onmouseup = (event) => {on_MouseUp('up_button')};

btn_off.onmousedown = (event) => {on_MouseDown('down_button')};
btn_off.onmouseup = (event) => {on_MouseUp('down_button')};



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
    
}

function on_MouseDown(button){
timeout = setTimeout (() =>{
    base.log(button +" pressed long");
    pressed_long = true
    base.setStateValue(button,true);
  },long_pressed_duration);
}

function on_MouseUp(button){
  clearTimeout(timeout)

  // button pressed long
  if (pressed_long){
    pressed_long = false;
    base.setStateValue(button,false);
  }
  // button pressed short
  else{
    base.log(button + " pressed short");
    if (button == 'up_button')
      base.setStateValue('state',true);
    else{
      base.setStateValue('state',false)
    }
    
  }
}