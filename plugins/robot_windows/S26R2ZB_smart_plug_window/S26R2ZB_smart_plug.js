/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const lbl_state = document.querySelector("#label_state");

const btn_switch = document.querySelector("#btn_switch");

let reset_counter = 0;

let default_btn_background = null;
let default_btn_text = null;
let state_on = false; 


btn_switch.addEventListener('click', () => switchState());



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
    setState(base.getStateValue('on'));
}

function setState(state){
    state_on = state
    if (state){
        lbl_state.style.background = "green"
        lbl_state.innerHTML = "ON"
        btn_switch.innerHTML = "Switch Off"
    }else{
        lbl_state.style.background = "red"
        lbl_state.innerHTML = "OFF"
        btn_switch.innerHTML = "Switch On"
    }
}
function switchState(){
    base.setStateValue('on',!state_on)
}
