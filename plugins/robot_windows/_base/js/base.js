// Log a message in the console widget.
  // Initialize the Webots window class in order to communicate with the robot.
window.onload = function() {
    // log('HTML page loaded.');
    window.robotWindow = webots.window();
    window.robotWindow.setTitle('Custom HTML robot window');
    window.robotWindow.receive = on_message;
    window.robotWindow.send("---- WINDOW LOADED ----");
};
  
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

function showStates(dict){
    var ul = document.getElementById('state_list');

    while (ul.firstChild) {
        ul.removeChild(ul.firstChild);
    }
    Object.entries(dict["data"]).forEach(entry => {
        const [key, value] = entry;
        // log(key +  " " + value);
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(`${key}: ${value}`));
        ul.appendChild(li);
      });
        
    
}