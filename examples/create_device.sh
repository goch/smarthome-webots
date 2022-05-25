#!/bin/bash

remove_device()
{
    rm -rf ../controllers/$1Controller
    rm -rf ../plugins/robot_windows/$1_window
    rm -rf ../SHDevices/sh_$1.py
    rm -rf ../protos/$1.proto
}

if (($# < 1)); then
    echo "DEVICE NAME REQUIRED"
    echo "create_device <DEVICE_NAME>"
    exit
fi

if [ $1 = "rm" ]; then
    echo "REMOVE DEVICE $2"
    remove_device "$2"
    exit
fi

echo "CREATE NEW DEVICE: " $1

echo "DEVICE CONTROLLER"
cp -r robot_controller ../controllers/$1Controller
mv ../controllers/$1Controller/sh_controller_template.py ../controllers/$1Controller/$1Controller.py

sed -i "s/from SHDevices.sh_shutter/from SHDevices.sh_$1/g" ../controllers/$1Controller/$1Controller.py
sed -i "s/sh_device = SH_Shutter/sh_device = SH_$1/g" ../controllers/$1Controller/$1Controller.py


echo "DEVICE WINDOW"
cp -r robot_window ../plugins/robot_windows/$1_window
workdir=../plugins/robot_windows/$1_window
mv $workdir/device_window.html $workdir/$1_window.html
mv $workdir/device.js $workdir/$1.js 

sed -i "s/script src=\"device.js\"/script src=\"$1.js\"/g" $workdir/$1_window.html 

echo "DEVICE LOGIC"
cp sh_device/sh_device_template.py ../SHDevices/sh_$1.py
sed -i "s/SH_Template/SH_$1/g" ../SHDevices/sh_$1.py 

echo "DEVICE PROTO"
cp proto/sh_device.proto ../protos/$1.proto

sed -i "s/PROTO Template/PROTO $1/g" ../protos/$1.proto
sed -i "s/    field SFString      name \"SH_DEVICE\"/    field SFString      name \"$1\"/g" ../protos/$1.proto

sed -i "s/    controller \"TemplateController\"/    controller \"$1Controller\"/g" ../protos/$1.proto
sed -i "s/    window \"Template_window\"/    window \"$1_window\"/g" ../protos/$1.proto

echo "DONE"

