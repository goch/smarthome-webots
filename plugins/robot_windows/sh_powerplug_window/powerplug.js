/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const lbl_currentPower = document.querySelector("#currentPowerConsumption");
const lbl_state = document.querySelector("#label_state");
const lbl_totalPower = document.querySelector("#totalPowerConsumotion");
const btn_reset = document.querySelector("#btn_reset");
const btn_switch = document.querySelector("#btn_switch");

let reset_counter = 0;

let default_btn_background = null;
let default_btn_text = null;
let state_on = false; 

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
    setCurrentPower(getStateValue('currentPowerConsumption'));
    setTotalPower(getStateValue('energyCounter'));
    setState(getStateValue('on'));
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
    setStateValue('on',!state_on)
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
        setStateValue('resetEnergyCounter',true);
        btn_reset.style.background = "green";
        btn_reset.innerHTML = "RESET OK!";
    }
}

