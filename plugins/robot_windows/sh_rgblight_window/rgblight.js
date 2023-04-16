/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */
import * as base from "../_base/js/base.js"

const btn_on = document.querySelector("#btn_on");
const btn_off = document.querySelector("#btn_off");

btn_on.onclick = (event) => {rgbOn(true)};
btn_off.onclick = (event) => {rgbOn(false)};

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
//subscribe to incoming messages
base.subscribe("object", onObjectMessage);
base.subscribe("state", onStateMessage);
base.subscribe("reset", onResetMessage);

//initialize WebUI
function init(){
  updateUI();
}


//update User Interface
function updateUI(){
    
}

function rgbOn(state){
  base.setStateValue('on', state);
}

// Box & hue slider
var boxPicker = new iro.ColorPicker("#boxPicker", {
    width: 400,
    color: "rgb(255, 0, 0)",
    borderWidth: 1,
    borderColor: "#fff",
    layout: [
        {
        component: iro.ui.Box,
        },
        {
        component: iro.ui.Slider,
        options: {
            id: 'hue-slider',
            sliderType: 'hue'
        }
        },
        
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
    
      boxPicker.on('color:change', function(color) {
        if (!limitcall(250))
          return;
        // log the current color as a HEX string
        //log("Color: " + color.hexString)
        // $('#r-value').html(parseInt(color.rgb.r));
        // $('#g-value').html(parseInt(color.rgb.g));
        // $('#b-value').html(parseInt(color.rgb.b));
        // $('#h-value').html(parseInt(color.hsv.h));
        // $('#s-value').html(parseInt(color.hsv.s));
        // $('#v-value').html(parseInt(color.hsv.v));
        // $('#kelvin-value').html("-");
    
        base.log("new Color: " + color.hexString + ' -> ', color.rgb.r + "," + color.rgb.g + "," + color.rgb.b )
        
        //TODO send all data at once
        //setStateValue("r", color.rgb.r/255 );
        //setStateValue("g", color.rgb.g/255 );
        //setStateValue("b", color.rgb.b/255 );
        
        base.setStateValue('color',color.hexString);
        
        //setState(lampid+'.brightness',parseInt(color.hsv.v));
        //setState(lampid+'.color',color.hexString)
        
        
      });
    
      kelvinPicker.on('color:change', function(color) {
        if (!limitcall(250))
          return;
        // log the current color as a HEX string
        // console.log(color.kelvin);
        // $('#r-value').html(parseInt(color.rgb.r));
        // $('#g-value').html(parseInt(color.rgb.g));
        // $('#b-value').html(parseInt(color.rgb.b));
        // $('#h-value').html(parseInt(color.hsv.h));
        // $('#s-value').html(parseInt(color.hsv.s));
        // $('#v-value').html(parseInt(color.hsv.v));
        // $('#kelvin-value').html(parseInt(color.kelvin));
        
        base.log("Temperature: " + color.kelvin);
        base.setStateValue('colortemp',color.kelvin);
    });