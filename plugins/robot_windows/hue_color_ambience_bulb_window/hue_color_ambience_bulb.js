/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

 const effectBox = document.querySelector("#effect_box");
 const btn_on = document.querySelector("#btn_on");
 const btn_off = document.querySelector("#btn_off");

 btn_on.onclick = (event) => {rgbOn(true)};
 btn_off.onclick = (event) => {rgbOn(false)};

 let lastcolor = "#FFFFFF"
 let timeout = null;
 let initialized = false

// A message coming from the robot has been received.
// new object message received
const onObjectMessage = (message) => {
  init();
}
// new state message received
const onStateMessage = (message) => {
  updateUI();
}
// new reset message received
const onResetMessage = (message) => {

}
//register callbacks for incoming messages
base.subscribe("object", onObjectMessage);
base.subscribe("state", onStateMessage);
base.subscribe("reset", onResetMessage);

//initialize WebUI
function init(){

  effectBox.onchange = function() {effectChange(effectBox.value)};

  boxPicker.on('color:change', function(color) {
    if (!limitcall(250))
      return;

    base.log("new Color: " + color.hexString + ' -> ', color.rgb.r + "," + color.rgb.g + "," + color.rgb.b )
    base.setStateValue('color',color.hexString);
  });

  kelvinPicker.on('color:change', function(color) {
    if (!limitcall(250))
      return;

    base.log("Temperature: " + color.kelvin);
    base.setStateValue('colortemp',color.kelvin);
});


brightnessPicker.on('color:change', function(color) {
  if (!limitcall(250))
    return;

  base.log("Brightness: " + color.value);
  base.setStateValue('brightness',color.value);
});

  updateUI();
}
//update User Interface
function updateUI(){
  
}

function rgbOn(state){
  base.setStateValue('on', state);
}

function effectChange(data){

  switch (data) {
    case "okay":
      base.setStateValue('effect', "okay")
      this.lastcolor = base.getStateValue('color');
      base.setStateValue('color', "#00ff00")
      
      this.timeout = setTimeout(okay, 5000);
      break;
    case "blink":
      //setStateValue('effect', "blink");
      break;
    case "breath":
      //setStateValue('effect', "breath");
      break;
    case "finish_effect":
      base.setStateValue('effect', "finish_effect");
      break;
    case "stop_effect":
      base.setStateValue('effect', "stop_effect");
      break;
    case "channel_change":
      base.setStateValue('effect', "channel_change");
      this.lastcolor = base.getStateValue('color');
      base.setStateValue('color', "#ff9900");
      this.timeout = setTimeout(channel_change, 8500);

      break;
      
  
    default:
      break;

  }
}
function okay(){
  clearTimeout(this.timeout);
  base.setStateValue('color', this.lastcolor)
}

function channel_change(){
  clearTimeout(this.timeout);
  base.setStateValue('color', this.lastcolor)
}


function breath(){
  clearTimeout(this.timeout);
  base.setStateValue('color', this.lastcolor)
}

// Box & hue slider
var boxPicker = new iro.ColorPicker("#boxPicker", {
  width: 400,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
  layout: [
      {
      component: iro.ui.Wheel,
      options: {
        wheelLightness: false
      }
      },
      {
      component: iro.ui.Slider,
      options: {
          id: 'hue-slider',
          sliderType: 'hue'
      }
      },
      {
        component: iro.ui.Slider,
      options: {
        // can also be 'saturation', 'value', 'red', 'green', 'blue', 'alpha' or 'kelvin'
        sliderType: 'saturation'
      }
      }
      
  ]
  });

  
  // Temperature
var kelvinPicker = new iro.ColorPicker("#kelvinPicker", {
  width: 400,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
  layoutDirection: 'vertical',
  layout: [
      {
      component: iro.ui.Slider,
      options: {
          sliderType: 'kelvin',
          sliderSize: 30,
          minTemperature: 1900,
          maxTemperature: 7000,
      }
      },
  ]
  });


  var brightnessPicker = new iro.ColorPicker("#brightnessPicker", {
    width: 400,
    color: "rgb(255, 255, 255)",
    borderWidth: 1,
    borderColor: "#fff",
    layoutDirection: 'vertical',
    layout: [
        
          {
            component: iro.ui.Slider,
          options: {
            // can also be 'saturation', 'value', 'red', 'green', 'blue', 'alpha' or 'kelvin'
            sliderType: 'value'
          }
        },
    ]
    });


  var last = +new Date();    
  function limitcall(time_ms){
    const now = +new Date();
    if (now - last > time_ms) { // 100ms
      last = now;
      //run function
      return true;
      //skip function
    }else return false;
  
  }
  
