#!/bin/bash

list_of_packages='xorg openbox lightdm chromium-browser unclutter avahi-daemon'

url=$1
user=$2

if [ -z $url ]
then
    echo "Please provide a url"
    exit
fi

if [ -z $user]
then
    echo "Please provide a username"
    exit
fi

apt update
apt install --assume-yes $list_of_packages

mkdir --parents ~/.config/openbox

cp /etc/xdg/openbox/autostart ~/.config/openbox

cat <<EOF >> ~/.config/openbox/autostart
xset s off -dpms &
unclutter -idle 0 &
chromium-browser --incognito --start-fullscreen --maximised $url &
EOF

cat <<EOF >> /etc/lightdm/lightdm.conf
[SeatDefaults]
autologin-user=$user
autologin-user-timeout=0
EOF

while true; do
    read -p "Do you want to reboot now?[y/n]" yn
    case $yn in
        [Yy]* ) reboot;;
        [Nn]* ) exit;;
        * ) echo "Please answer with y or n.";;
    esac
done
