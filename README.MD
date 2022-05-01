# Install

- Webots 2022a


source env/bin/activate

pip install requirements

export Location to pythonpath

export WEBOTS_HOME=/usr/local/webots
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${WEBOTS_HOME}/lib/controller

# add project path to pythonpath

export PYTHONPATH=$PYTHONPATH:$WEBOTS_HOME/lib/controller/python39:~/bachelor_ws/spot



