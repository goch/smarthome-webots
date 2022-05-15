/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const lbl_currentPower = document.querySelector("#currentPowerConsumption");
const lbl_state = document.querySelector("#label_state");
const lbl_totalPower = document.querySelector("#totalPowerConsumotion");
const btn_reset = document.querySelector("#btn_reset");
const btn_switch = document.querySelector("#btn_switch");

let reset_counter = 0;

let default_btn_background = null;
let default_btn_text = null;
let state_on = false; 


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
    sendState('on',!state_on)
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
        sendState("resetEnergyCounter",true);
        btn_reset.style.background = "green";
        btn_reset.innerHTML = "RESET OK!";
    }




}
// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            showStates(msg);
            data = msg['data'];
            label_device_name.innerHTML = msg['name']; 
            setCurrentPower(data["currentPowerConsumption"]);
            setTotalPower(data["energyCounter"]);
            setState(data["on"]);
            
        } catch (e) {}
    }
}

