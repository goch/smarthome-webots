# Smart Home Simulation for Webots

This project is a smart home simulation for the Webots simulator. It allows you to create a custom 3D environment and add smart home devices to it. You can then connect to smart home broker software such as iobroker. The project is also extendable to other frameworks such as ROS2 and Home Assistant.

![rockinhome_extended](https://user-images.githubusercontent.com/8045402/232316547-a1e4c802-64c3-4f3e-a6aa-92e02e1ec717.png)

<img src="https://user-images.githubusercontent.com/8045402/232316660-f1b7db59-1d59-4bb1-92b9-daf98bf6204b.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/8045402/232316669-a211f005-f55a-4aed-af1f-76450792da49.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/8045402/232316679-1bd36ef4-b8ad-4998-99c8-e2f28af8c8ef.png" width="30%"></img> 

# Install

## Prerequisites

- Webots 2023a -> https://github.com/cyberbotics/webots/releases/tag/R2023a
- python 3.10
- git


## Ubuntu 22.04

```bash
sudo apt install git python3.10-venv
git clone https://github.com/goch/smarthome-webots.git
cd smarthome-webots
python3 -m venv env
echo export PYTHONPATH=$PWD:$PYTHONPATH >> env/bin/activate
source env/bin/activate
pip install -r requirements.txt

webots worlds/home.wbt
```
<!-- ## Fedora 39
```bash
sudo dnf install git python python-pip
git clone https://github.com/goch/smarthome-webots.git
cd smarthome-webots
pip install virtualenv
python -m venv env
echo export PYTHONPATH=$PWD:$PYTHONPATH >> env/bin/activate
source env/bin/activate
pip install -r requirements.txt

webots worlds/home.wbt
``` -->


<!-- ## Arch

```bash
sudo pacman -S git python python-pip

git clone https://github.com/goch/smarthome-webots.git
cd smarthome-webots
pip install virtualenv
python -m venv env
pip install -r requirements.txt
echo export $PYTHONPATH:$PWD >> env/bin/activate
source env/bin/activate

webots worlds/home.wbt
``` -->

## Manjaro
```bash
sudo pacman -S git python python-pip
git clone https://github.com/goch/smarthome-webots.git
cd smarthome-webots
pip install virtualenv
python -m venv env
echo export PYTHONPATH=$PWD:$PYTHONPATH >> env/bin/activate
source env/bin/activate
pip install -r requirements.txt

webots worlds/home.wbt
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






### install virtualenvironment
```bash
pip install virtualenv
python -m venv env

source env/bin/activate
```


### Open simulated environment

start webots

File -> Open World 

you can find demo worlds in this location:

```bash
C:\Users\<Username>\smarthome-webots\worlds\empty.wbt
```





