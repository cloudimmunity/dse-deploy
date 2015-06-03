#! /bin/bash

curl -L https://debian.datastax.com/debian/repo_key | sudo apt-key add -
sudo apt-get update
sudo apt-get -y  install dse-full
sudo apt-get -y  install opscenter
hname=$(date +'dse-node-%m%d%y%H%M%S')
sudo hostname $hname
sudo echo "$hname" > /etc/hostname
sudo echo "127.0.0.1 $hname" >> /etc/hosts

