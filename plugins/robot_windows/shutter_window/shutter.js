/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */


const slider = document.querySelector("#shutter_slider");
const slider_output = document.querySelector("#shutter_position");
const progressbar = document.querySelector("#ShutterPositionProgressBar");

slider.addEventListener ("change", function () {
  log("changeEvent triggered -> " + this.value);
  setSlider(this.value);
  sendState('setPosition', to_motor(this.value));
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


  // The window user has toggled the "Stop motors" checkbox.
  // This information is sent to the robot.
function toggleStopCheckbox(obj) {
    if (obj.checked) {
      obj.parentNode.classList.add('checked');
      obj.parentNode.lastChild.innerHTML = 'Start Motors';
      window.robotWindow.send('stop motors');
      log('Stop motors.');
    } else {
      obj.parentNode.classList.remove('checked');
      obj.parentNode.lastChild.innerHTML = 'Stop Motors';
      window.robotWindow.send('release motors');
      log('Release motors.');
    }
  }
  
  // A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            showStates(msg);
            log(msg["data"]["currentPosition"])
            setSlider(to_percent(msg["data"]["setPosition"]))
            setProgressBar(to_percent(msg["data"]["currentPosition"]))

            document.getElementById('device_name').innerHTML = msg['name'];
        } catch (e) {}
    }
}


