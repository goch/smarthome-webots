/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const console_list = document.querySelector("#console");
const lbl_armed = document.querySelector("#lbl_armed");
const lbl_triggered = document.querySelector("#lbl_triggered");
//const btn_lamp = document.querySelector("#btn_lamp");
const lbl_brightness = document.querySelector("#lbl_brightness");

//btn_on_default_color = btn_lamp.style.background
triggered_default_color = lbl_triggered.style.background

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
  setlblArmed(getStateValue('armed'));
  setlblTriggered(getStateValue('triggered'));
}

function setlblArmed(armed){
  if (armed){
    lbl_armed.style.background = "red";
    lbl_armed.innerHTML = "ARMED!";
  }else{
    lbl_armed.style.background = "green";
    lbl_armed.innerHTML = "DISABLED<br> <small>click to arm</small>";
  }
}

function setlblTriggered(triggered){
  if (triggered){
    lbl_triggered.innerHTML = "True";

    if (getStateValue('on')){
      lbl_triggered.style.background = "red";
    }else{   
      lbl_triggered.style.background = triggered_default_color;
    } 

  }else{
    lbl_triggered.style.background = "green";
    lbl_triggered.innerHTML = "False";
  }
}

function setBtnLamp(lamp_on){
  if (lamp_on){
    btn_lamp.style.background = "red";
    btn_lamp.innerHTML = "ON";

  }else{
    btn_lamp.style.background = btn_on_default_color;
    btn_lamp.innerHTML = "OFF";
  }
}

function setLabelBrightness(brightness){

}

lbl_armed.addEventListener ("click", function () {
  setlblArmed( !getStateValue('armed')) 
  setStateValue('armed', !getStateValue('armed') )
});

// btn_lamp.addEventListener ("click", function () {
//   lamp_on = !getStateValue('on');
//   setStateValue('on',lamp_on)
// });
