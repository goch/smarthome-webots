/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const label_luminosity = document.querySelector("#label_luminosity");



function setLuminosity(value){
    label_luminosity.innerHTML = value.toFixed(2) + " W/m²";
}

// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            showStates(msg);
            label_device_name.innerHTML = msg['name'];
            let luminosity = msg['data']['luminosity'];
            if (!isNaN(luminosity)){
                setLuminosity(luminosity);
                
            }else
                setLuminosity(-1);
        } catch (e) {}
    }
}

