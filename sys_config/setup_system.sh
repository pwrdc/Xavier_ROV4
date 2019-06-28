#!/bin/bash
sudo apt-get update
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
sudo apt-get install python3-pip python3-flask
sudo pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta
sudo pip3 install -U pip
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu
sudo apt-get install gcc build-essential libcurl4-openssl-dev libglib2.0-dev glib-networking libssl-dev asciidoc
wget https://megatools.megous.com/builds/megatools-1.10.2.tar.gz
tar -xvzf megatools-1.10.2.tar.gz
cd megatools-1.10.2 && ./configure --disable-shared
cd megatools-1.10.2 && make && sudo make install

