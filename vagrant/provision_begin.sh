#! /bin/bash

sudo apt-get update
sudo apt-get -y install python-software-properties python g++ make
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install git
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
sudo echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
sudo apt-get -y install oracle-java7-installer
sudo update-java-alternatives -s java-7-oracle
sudo apt-get -y install libjna-java
sudo apt-get -y install htop
sudo apt-get -y install sysstat
sudo apt-get -y install iftop
sudo apt-get -y install binutils
sudo apt-get -y install pbzip2
sudo apt-get -y install zip
sudo apt-get -y install unzip
sudo apt-get -y install curl
sudo apt-get -y install tree
sudo apt-get -y install dstat
sudo apt-get -y install ethtool
sudo apt-get -y install openssl
sudo apt-get -y install ruby
sudo apt-get -y install libopenssl-ruby
sudo echo vm.max_map_count = 131072 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
