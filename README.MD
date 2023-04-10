# Smart Home Simulation for Webots

This project is a smart home simulation for the Webots simulator. It allows you to create a custom 3D environment and add smart home devices to it. You can then connect to smart home broker software such as iobroker. The project is also extendable to other frameworks such as ROS2 and Home Assistant.

# Install


## Linux

- Webots 2023a
- python 3.10


### export Location to pythonpath

```bash
export WEBOTS_HOME=/usr/local/webots
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${WEBOTS_HOME}/lib/controller
```

### clone smarthome_webots repo

```bash
git clone https://github.com/goch/smarthome-webots.git
```
### add project path to pythonpath
```bash
export PYTHONPATH=$PYTHONPATH:$WEBOTS_HOME/lib/controller/python310:~/smarthome_webots
```
### Install requirements
```bash
pip install virtualenv
python -m venv env

source env/bin/activate
pip install -r requirements.txt
```

## Windows

### install python 3.10 

Download and install Python 3.10. On the first page, at the bottom, check "Add Python 3.10 to PATH!" and disable PATH limit.

https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

### Download git for windows
Download git for windows
https://github.com/git-for-windows/git/releases/download/v2.40.0.windows.1/Git-2.40.0-64-bit.exe


###  webots 2023a  

download and follow install instructions at 
https://cyberbotics.com/doc/guide/installation-procedure#installation-on-windows



### clone repository 
clone this repository using git bash
```bash
git clone https://github.com/goch/smarthome-webots.git
```




### Add Project Path to PythonPath 
switch into the repository and set your pythonpath

```bash
cd smarthome-webots
setx PYTHONPATH $(pwd)
```
### Install requirements

install project requirements
```bash
pip install -r requirements.txt
```




## Optional

### install virtualenvironment
```bash
pip install virtualenv
python -m venv env

source env/bin/activate
```

# Open Simulated Environment

start webots

File -> Open World 

you can find demo worlds in this location:

```bash
C:\Users\<Username>\smarthome-webots\worlds\empty.wbt
```





