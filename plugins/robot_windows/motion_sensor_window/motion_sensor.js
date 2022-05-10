/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

const label_device_name = document.querySelector("#device_name");
const label_motion_detected = document.querySelector("#motion_detected");

function setMotionDetected(motion_detected){
    label_motion_detected.innerHTML = motion_detected.toString();
    if (motion_detected){
        label_motion_detected.style.background = "green";
    }else{
        label_motion_detected.style.background = "red";
    } 
}

// A message coming from the robot has been received.
function on_message(message) {
    if (message != null){
        try {
            msg = JSON.parse(message)
            window.robotWindow.setTitle(msg['name']);
            label_device_name.innerHTML = msg['name'];
            showStates(msg);
            setMotionDetected(msg['data']["motion_detected"])
        } catch (e) {}
    }
}

