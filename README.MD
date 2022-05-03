# Install

- Webots 2022a
- python 3.10+

pip install virtualenv
python3 -m venv env

source env/bin/activate
pip install -r requirements.txt





#export Location to pythonpath

export WEBOTS_HOME=/usr/local/webots
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${WEBOTS_HOME}/lib/controller

# add project path to pythonpath

export PYTHONPATH=$PYTHONPATH:$WEBOTS_HOME/lib/controller/python39:~/bachelor_ws/smarthome_webots



