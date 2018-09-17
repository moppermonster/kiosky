#!/bin/bash

list_of_packages = 'xorg openbox lightdm chromium-browser unclutter avahi-deamon'

url = $1
user = $2

apt update
apt install --assume-yes $list_of_packages

mkdir --parents ~/.config/openbox

cp /etc/xdg/openbox/autostart ~/.config/openbox

cat <<EOF >> ~/.config/openbox/autostart
xset s off -dpms &
unclutter -idle 0 &
chromium-browser --incognito --start-fullscreen --maximised $url &
EOF

sed -i 's./.*#autologin-user=.*/c\autologin-user='"$user" /etc/lightdm/lightdm.conf
sed -1 '/autologin-user-timeout=0/s/^#//g' /etc/lightdm/lightdm.conf

while true; do
    read -p "Do you want to reboot now?[y/n]"yn
    case $yn in
        [Yy]* ) reboot;;
        [Nn]* ) exit;;
        * ) echo "Please anser with y or n.";;
    esac
done
