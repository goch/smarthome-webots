import RobotWindow from 'https://cyberbotics.com/wwi/R2023a/RobotWindow.js';
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
let onObjectMessage;
let onStateMessage;
let onResetMessage;

let deviceName = null
let states = {}

let debug_list = null;
let state_list = null;
let label_device_name = null;



  // Initialize the Webots window class in order to communicate with the robot.
window.onload = function() {
    // log('HTML page loaded.');
//    window.robotWindow = webots.window();
    window.robotWindow = new RobotWindow();

    window.robotWindow.setTitle('Custom HTML robot window');
    window.robotWindow.receive = on_message;

    state_list = document.querySelector('#state_list');
    label_device_name = document.querySelector("#device_name");

    createStateList()
    sendText("---- WINDOW LOADED ----");
};


export function test(){
  console.log("test");
}

export function subscribe(type, f){
if (type === "object") onObjectMessage = f;
if (type === "state") onStateMessage = f;
if (type === "reset") onResetMessage = f;

}

export function register_OnObjectMessage(f){
  onObjectMessage = f;
}
export function register_OnStateMessage(f){
  onStateMessage = f;
}
export function register_OnResetMessage(f){
  onResetMessage = f;
}



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

export function setStateValue(name, value, send=true){
  if (!(name  in states)){
    log("Want to set State: "+name +" but state is not defined... yet");
    return;
  }

  name = resolveRemap(name)
  states[name].value = value;
  
  if (send){
    log("Sending " + name + " -> " + value )
    sendState(name,value)
  }
}

export function getStateValue(name){
  return states[resolveRemap(name)].value
}

function resolveRemap(name){
  if (states[name].remap === null){
    return name;
  }else return states[name].remap;
}

function on_message(message){
  if (message == null) return;

  try {
    const msg = JSON.parse(message);
    
    switch (msg.type) {
      case 'object':
        initStates(msg);
        onObjectMessage(msg);
        break;
      case 'state':
        setStateValue(msg.data.name, msg.data.value, false);
        showStates();
        onStateMessage(msg);
        break;
      case 'reset':
        log("RESET MESSAGE NOT YET IMPLEMENTED!");
        onResetMessage(msg);
        break;					
      default:
        break;
    }
  } catch (e) {
    
    log("EXCEPTION:  " + e.message + " -> " + message)
    throw(e)
    
  }
}
  
export function log(message) {
    var console = document.getElementById('console');
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    console.prepend(li);
 }

 function logState(state){
  Object.entries(state).forEach(entry => {
    const [key, value] = entry;
    log(key +': ' + value)
  });
 }

function sendState(stateName, val){
    let msg = {property: stateName, value: val}
    window.robotWindow.send(JSON.stringify(msg))
}

function sendText(data){
  window.robotWindow.send(data);
}

function showStates(){
  while (debug_list.firstChild) {
    debug_list.removeChild(debug_list.firstChild);
  }

    Object.entries(states).forEach(entry => {
      const [name, state] = entry;
      if (state['remap'] != null)
        return;

      var row = document.createElement('div');
      row.setAttribute('class','row');

      var name_elem = document.createElement('div');
      name_elem.setAttribute('class','column');
      name_elem.style.width = '60%';
      name_elem.appendChild(document.createTextNode(`${name}:`))

      var value_elem = document.createElement('div');
      value_elem.setAttribute('class','column');
      value_elem.style.width = '20%';

       var elem = null;
       var datatype = typeof(state.value)
      if (datatype == "boolean"){
        elem = createBooleanElement(name, state.value)
      }else if (datatype == "string") {
        elem = createStringElement(name, state.value)
      }else{ // number
        elem = createNumberElement(name, state.value)
      }

      value_elem.appendChild(elem);

      row.appendChild(name_elem);
      row.appendChild(value_elem);

      debug_list.appendChild(row);
    });
}

function createStringElement(name, value){
  var input = document.createElement('input');
      input.setAttribute('type','text');
      //input.setAttribute('maxlength','3');
      //input.setAttribute('size','10');
      input.setAttribute('value', value);
      input.onchange = (event) => {setStateValue( name, event.target.value)};
  return input;
}

function createNumberElement(name, value){
  var input = document.createElement('input');
      input.setAttribute('type','number');
      input.setAttribute('maxlength','3');
      input.setAttribute('size','3');
      input.setAttribute('value', value);
      input.onchange = (event) => {setStateValue( name, Number(event.target.value))};
  return input;
}

function createBooleanElement(name, value){
  var label = document.createElement('label');
      label.setAttribute('class','switch');

      var input = document.createElement('input');
      input.setAttribute('type','checkbox');
      
      input.onchange = (event) => {setStateValue( name, event.target.checked)};
      if (value) input.setAttribute('checked','');

      var checkbox = document.createElement('span');
      checkbox.setAttribute('class','slider round');

      label.appendChild(input);
      label.appendChild(checkbox);
return label;

}

/* Colapseable States*/
function createStateList(){

	let button =  document.createElement('button')
	button.setAttribute('class','collapsible');
  button.innerText = 'State List';

	debug_list = document.createElement('div');
  debug_list.setAttribute('class', 'content');
  debug_list.appendChild(document.createTextNode('content'));

	state_list.append(button);
	state_list.appendChild(debug_list);

  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

}

