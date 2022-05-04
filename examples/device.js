/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

      // Initialize the robot window
let last_pressed = -1;
let long_pressed_duration = 500


  
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
            document.getElementById('device_name').innerHTML = msg['name'];
        } catch (e) {}
        document.getElementById('message').innerHTML = message;
      }
}

function on_MouseDown(button){
    last_pressed = new Date().getTime();
    log(button + ": MouseDown " + last_pressed);
}

function on_MouseUp(button){
    current_pressed = new Date().getTime();
    log(button + ": MouseUp " + current_pressed);

    let name =""
    if (current_pressed - last_pressed >= long_pressed_duration){
        name = button +"_pressed_long";
    }else{
        name = button +"_pressed_short";
    }

    log(name)
    sendState(name,true);
    reset_button(name,200);
}

function reset_button(name,duration){
    setTimeout(() => {
        sendState(name, false)
    }, duration);
}