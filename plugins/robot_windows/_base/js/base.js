let deviceName = null
let states = {}

let debug_list = null;
let state_list = null;
let label_device_name = null;

  // Initialize the Webots window class in order to communicate with the robot.
window.onload = function() {
    // log('HTML page loaded.');
    window.robotWindow = webots.window();
    window.robotWindow.setTitle('Custom HTML robot window');
    window.robotWindow.receive = on_message;

    state_list = document.querySelector('#state_list');
    label_device_name = document.querySelector("#device_name");

    createStateList()
    sendText("---- WINDOW LOADED ----");
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
  name = resolveRemap(name)
  states[name].value = value;
  
  if (send){
    log("Sending " + name + " -> " + value )
    sendState(name,value)
  }
}

function getStateValue(name){
  return states[resolveRemap(name)].value
}

function resolveRemap(name){
  if (states[name].remap != null){
    return states[name].remap;
  }else return name
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
    log("EXCEPTION:  " + e + " -> " + message)
  }
}
  
function log(message) {
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
    msg = {property: stateName, value: val}
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
       datatype = typeof(state.value)
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
      input.setAttribute('onchange','setStateValue("'+ name +'", this.value)');
  return input;
}

function createNumberElement(name, value){
  var input = document.createElement('input');
      input.setAttribute('type','number');
      input.setAttribute('maxlength','3');
      input.setAttribute('size','3');
      input.setAttribute('value', value);
      input.setAttribute('onchange','setStateValue("'+ name +'", +(this.value))');
  return input;
}

function createBooleanElement(name, value){
  var label = document.createElement('label');
      label.setAttribute('class','switch');

      var input = document.createElement('input');
      input.setAttribute('type','checkbox');
      input.setAttribute('onchange','setStateValue("'+ name +'", this.checked)');
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
