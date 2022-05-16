let deviceName = null
let states = {}

let ul = null;
let label_device_name = null;

  // Initialize the Webots window class in order to communicate with the robot.
window.onload = function() {
    // log('HTML page loaded.');
    window.robotWindow = webots.window();
    window.robotWindow.setTitle('Custom HTML robot window');
    window.robotWindow.receive = on_message;
    sendText("---- WINDOW LOADED ----");

    ul = document.querySelector('#state_list');
    label_device_name = document.querySelector("#device_name");
};

function initStates(dict){
  log("Initializing States:");
  
  window.robotWindow.setTitle(dict.name);
  label_device_name.innerHTML = dict.name;
  
  Object.entries(dict.data).forEach(entry => {
      const [name, state] = entry;
      states[name] = state
    });

    showStates()
}

function setStateValue(name, value, send=true){
  states[name].value = value;
  
  if (send){
    sendState(name,value)
  }
}

function getStateValue(name){
  return states[name].value
}

function on_message(message){
  if (message == null) return;

  try {
    const msg = JSON.parse(message);
    
    switch (msg.type) {
      case 'object':
        initStates(msg);
        on_ObjectMessage(msg)
        break;
      case 'state':
        setStateValue(msg.data.name, msg.data.value, send=false)
        showStates()
        on_StateMessage(msg)
        break;
      case 'reset':
        log("RESET MESSAGE NOT YET IMPLEMENTED!")
        on_ResetMessage(msg)
        break;					
      default:
        break;
    }
  } catch (e) {
    log("EXCEPTION:  " + e)
  }

}
  
function log(message) {
    var ul = document.getElementById('console');
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    ul.prepend(li);
 }

function sendState(stateName, val){
    msg = {property: stateName, value: val}
    window.robotWindow.send(JSON.stringify(msg))
}

function sendText(data){
  window.robotWindow.send(data);
}


function showStates(){
  while (ul.firstChild) {
    ul.removeChild(ul.firstChild);
  }
    Object.entries(states).forEach(entry => {
      const [name, state] = entry;

      var li = document.createElement('li');
      li.appendChild(document.createTextNode(`${name}: ${state.value}`));
      ul.appendChild(li);
    });
}