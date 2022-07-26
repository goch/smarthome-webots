#!/bin/bash

get_proto_template()
{
    
proto=$(case $1 in
  "rgb_light") echo "RGBLight" ;;
  "motion_sensor") echo "MotionSensor" ;;
  "light_sensor") echo "LightSensor" ;;
  "power_plug") echo "PowerPlug" ;;
  "shutter") echo "Shutter" ;;
  "thermostat") echo "Thermostat" ;;
  "alarm") echo "Alarm" ;;
  "switch") echo "Button" ;;
  "distance") echo "DistanceSensor" ;;
  "co2_sensor") echo "CO2Sensor" ;;
  *) echo "Template not Found"; exit ;;
esac)
echo $proto

}

remove_device()
{
    if [ "$2" ]; then
        folder=$2/
    fi
 
    rm -rf ../controllers/$1Controller
    rm -rf ../plugins/robot_windows/$1_window
    rm -rf ../SHDevices/$folder'sh_'$1.py
    rm -rf ../protos/$folder$1.proto
}


if (($# < 1)); then
    echo "DEVICE NAME REQUIRED"
    echo "create_device <DEVICE_NAME> [ <MANUFACTURER> <TEMPLATE> ]"
    exit
fi

if [ $1 = "rm" ]; then
    echo "REMOVE DEVICE $3/$2"
    remove_device "$2" "$3"
    exit
fi

if [ $1 = "proto" ]; then
    proto=$(get_proto_template $2)
    echo $proto
    exit
fi

#create Manufacturer Folder
if [ "$2" ]; then
    mkdir ../protos/$2
    mkdir ../SHDevices/$2
    manufacturerDir="$2/"
fi

if [ "$3" ]; then
    template=$(get_proto_template $3)
fi



echo "CREATE NEW DEVICE: " $1
echo "MANUFACTURER: " $2
echo "TEMPLATE: " $template

classFilename=$(echo "$template" | tr '[:upper:]' '[:lower:]')


echo "DEVICE CONTROLLER"
cp -r robot_controller ../controllers/$1Controller
mv ../controllers/$1Controller/sh_controller_template.py ../controllers/$1Controller/$1Controller.py

if [ "$2" ]; then
importDir=$2.
fi

sed -i "s/from SHDevices.sh_shutter/from SHDevices.$importDir"sh_"$1/g" ../controllers/$1Controller/$1Controller.py
sed -i "s/sh_device = SH_Shutter/sh_device = SH_$1/g" ../controllers/$1Controller/$1Controller.py

if [ "$3" ]; then
    window='../plugins/robot_windows/sh_'$classFilename'_window'
    windowHtmlName='sh_'$classFilename'_window'
    windowjsname=$classFilename
else
    window=robot_window
    windowHtmlName=device_window
    windowjsname=device
fi 


echo "DEVICE WINDOW"
cp -r $window ../plugins/robot_windows/$1_window
workdir=../plugins/robot_windows/$1_window
mv $workdir/$windowHtmlName.html $workdir/$1_window.html
mv $workdir/$windowjsname.js $workdir/$1.js 

sed -i "s/script src=\"$windowjsname.js\"/script src=\"$1.js\"/g" $workdir/$1_window.html 

echo "DEVICE LOGIC"
cp sh_device/sh_device_template.py ../SHDevices/$manufacturerDir'sh_'$1.py


sed -i "s/from SHDevices.sh_device import/from SHDevices.sh_$classFilename import/g" ../SHDevices/$manufacturerDir'sh_'$1.py 
sed -i "s/class SH_Template(SHDevice):/class SH_$1(SH_$template):/g" ../SHDevices/$manufacturerDir'sh_'$1.py 

echo "DEVICE PROTO"

if [ "$3" ]; then
    proto=$(get_proto_template $3)
    proto="../protos/_GENERIC/SH_$proto.proto"
    protoID=SH_$template
    protoName=$template
    controllerName=$template'Controller'
    windowName=sh_$classFilename'_window'
    
else
   proto="proto/sh_device.proto" 
   protoID=Template
   protoName=SH_DEVICE
   controllerName=TemplateController
   windowName=Template_window
   
fi


cp $proto ../protos/$manufacturerDir$1.proto

sed -i "s/PROTO $protoID/PROTO $1/g" ../protos/$manufacturerDir$1.proto
sed -i "s/    field SFString      name \"$protoName\"/    field SFString      name \"$1\"/g" ../protos/$manufacturerDir$1.proto


sed -i "s/controller \"$controllerName\"/controller \"$1Controller\"/g" ../protos/$manufacturerDir$1.proto
sed -i "s/window \"$windowName\"/window \"$1_window\"/g" ../protos/$manufacturerDir$1.proto

echo "DONE"

