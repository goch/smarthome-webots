/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

// Initialize the robot window
let last_pressed = -1;
let long_pressed_duration = 500;
let multipress_timeout = 250;
let timeout = null;
let multipress_count = 0;
let buttons_generated = false;


// new object message received
function on_ObjectMessage(message){
  initUI(message.data);
}

// new state message received
function on_StateMessage(message){
  updateUI();
}
// new reset message received
function on_ResetMessage(message){

}

//setup User Interface
function initUI(data){
  generateButtons(data);  
  updateUI();
}
//update User Interface
function updateUI(){
  
}
  
function generateButtons(dict){
  if (buttons_generated) return;

  log("Generating Buttons");
  let btnlist = document.getElementById('buttonlist');
  let last_name = "";
  let btn_count = Object.keys(dict).length
  Object.entries(dict).forEach(entry => {
    const [key, value] = entry;
    
    let name = key.split('_')[0];
    if (name == last_name){
      return;
    } 

    var btn = document.createElement('button');
    btn.setAttribute("onmousedown", 'on_MouseDown("'+ name +'")');
    btn.setAttribute("onmouseup", 'on_MouseUp("'+ name +'")');
    btn.style.width = 100/btn_count +"%";
    btn.innerHTML = name;
    last_name = name;
    
    btnlist.appendChild(btn);
    
  });
  buttons_generated = true;

}

function on_MouseDown(button){
    last_pressed = new Date().getTime();
}

function on_MouseUp(button){
    current_pressed = new Date().getTime();
    multipress_count++;

    let time_since_press = current_pressed - last_pressed;
    let name ="";
    if ( time_since_press >= long_pressed_duration){
        name = button +"_pressed_long";
        multipress_count = 0;
        log(name);
        setStateValue(name,true);
        reset_button(name,200);
    
    }else if (timeout == null){
      
        timeout = setTimeout(() => {
        
          if (multipress_count >= 2){
            name = button +"_pressed_double"; 
          } else {
            name = button +"_pressed_short"; 
          }

          log(name);
          setStateValue(name,true);
          reset_button(name,200);

          timeout = null;
          multipress_count = 0;
      
        }, multipress_timeout);
    }
      
      
}

function reset_button(name,duration){
    setTimeout(() => {
      setStateValue(name, false)
    }, duration);
}