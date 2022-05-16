/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */


const slider = document.querySelector("#shutter_slider");
const slider_output = document.querySelector("#shutter_position");
const progressbar = document.querySelector("#ShutterPositionProgressBar");

const btn_open = document.querySelector('#btn_open');
const btn_close = document.querySelector('#btn_close');
const btn_up = document.querySelector('#btn_up');
const btn_down = document.querySelector('#btn_down');
const btn_stop = document.querySelector('#btn_stop');

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
  setSlider( to_percent( getStateValue('setPosition')));
  setProgressBar( to_percent(getStateValue('currentPosition')));
}

slider.addEventListener ("change", function () {
  log("changeEvent triggered -> " + this.value);
  setSlider(this.value);
  setStateValue('setPosition', to_motor(this.value));
});


btn_up.addEventListener ("click", function () {
  setStateValue('up',true);
});

btn_down.addEventListener ("click", function () {
  setStateValue('down',true);
});

btn_stop.addEventListener ("click", function () {
  setStateValue('stop',true);
});

btn_open.addEventListener ("click", function () {
  sendText('WINDOW_OPEN');
});

btn_close.addEventListener ("click", function () {
  sendText('WINDOW_CLOSED');
});

  function setSlider(value){
  slider.value = value;
}

function setProgressBar(value){
  progressbar.style.width = value + "%";
  slider_output.innerHTML = value + "%"; 
}

function setCurrentPosition(){
  slider_output.innerHTML = value + "%";
}

function to_percent(value){
  return ((value/1.3) * 100).toFixed(0);
}

function to_motor(value){
  return (value/100) * 1.3;
}