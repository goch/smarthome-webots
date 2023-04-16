/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const lbl_currentPower = document.querySelector("#currentPowerConsumption");
const lbl_state = document.querySelector("#label_state");
const lbl_totalPower = document.querySelector("#totalPowerConsumotion");
const btn_reset = document.querySelector("#btn_reset");
const btn_switch = document.querySelector("#btn_switch");

let reset_counter = 0;

let default_btn_background = null;
let default_btn_text = null;
let state_on = false; 


btn_switch.addEventListener('click', () => switchState());
btn_reset.addEventListener('click', () => resetEnergyCounter());


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
    setCurrentPower(base.getStateValue('currentPowerConsumption'));
    setTotalPower(base.getStateValue('energyCounter'));
    setState(base.getStateValue('on'));
}


function setCurrentPower(value){
    lbl_currentPower.innerHTML = "> " + value.toFixed(0) + " W";
}

function setTotalPower(value){
    lbl_totalPower.innerHTML = value.toFixed(3) + " kW/h";
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

function resetEnergyCounter(){
    reset_counter++;
    if (reset_counter <2){
        default_btn_text = btn_reset.innerHTML;
        default_btn_background = btn_reset.style.background;
        btn_reset.style.background = "red";
        btn_reset.innerHTML = "REALLY?";
        
        setTimeout(() => {
            reset_counter = 0;
            btn_reset.style.background = default_btn_background;
            btn_reset.innerHTML = default_btn_text;
        }, 3000);
        
    }else{
        base.setStateValue('resetEnergyCounter',true);
        btn_reset.style.background = "green";
        btn_reset.innerHTML = "RESET OK!";
    }
}

