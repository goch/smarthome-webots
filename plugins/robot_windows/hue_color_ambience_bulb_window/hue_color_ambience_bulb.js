/* global webots */
/* eslint no-unused-vars: ['error', { 'varsIgnorePattern': 'handleBodyLEDCheckBox|toggleStopCheckbox' }] */

 const effectBox = document.querySelector("#effect_box");
 let lastcolor = "#FFFFFF"
 let timeout = null;

// A message coming from the robot has been received.
// new object message received
function on_ObjectMessage(message){
  initUI();
}

// new state message received
function on_StateMessage(message){
updateUI();
}

// new reset message received
function on_ResetMessage(message){

}

//setup User Interface
function initUI(){
  
  updateUI();
}
//update User Interface
function updateUI(){
  
}

function rgbOn(state){
  setStateValue('on', state);
}

effectBox.onchange = function() {effectChange(effectBox.value)};

function effectChange(data){

  switch (data) {
    case "okay":
      setStateValue('effect', "okay")
      this.lastcolor = this.getStateValue('color');
      this.setStateValue('color', "#00ff00")
      
      this.timeout = setTimeout(okay, 5000);
      break;
    case "blink":
      //setStateValue('effect', "blink");
      break;
    case "breath":
      //setStateValue('effect', "breath");
      break;
    case "finish_effect":
      setStateValue('effect', "finish_effect");
      break;
    case "stop_effect":
      setStateValue('effect', "stop_effect");
      break;
    case "channel_change":
      setStateValue('effect', "channel_change");
      this.lastcolor = this.getStateValue('color');
      this.setStateValue('color', "#ff9900");
      this.timeout = setTimeout(channel_change, 8500);

      break;
      
  
    default:
      break;

  }
}
function okay(){
  clearTimeout(this.timeout);
  this.setStateValue('color', this.lastcolor)
}

function channel_change(){
  clearTimeout(this.timeout);
  this.setStateValue('color', this.lastcolor)
}


function breath(){
  clearTimeout(this.timeout);
  this.setStateValue('color', this.lastcolor)
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
  
    boxPicker.on('color:change', function(color) {
      if (!limitcall(250))
        return;

  
      log("new Color: " + color.hexString + ' -> ', color.rgb.r + "," + color.rgb.g + "," + color.rgb.b )

      setStateValue('color',color.hexString);
      

      
    });
  
    kelvinPicker.on('color:change', function(color) {
      if (!limitcall(250))
        return;

      
      log("Temperature: " + color.kelvin);
      setStateValue('colortemp',color.kelvin);
  });


  brightnessPicker.on('color:change', function(color) {
    if (!limitcall(250))
      return;

    
    log("Brightness: " + color.value);
    setStateValue('brightness',color.value);
});
