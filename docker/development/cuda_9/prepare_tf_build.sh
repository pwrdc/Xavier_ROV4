#!/bin/bash
pip3 install -U --user pip six numpy wheel setuptools mock
pip3 install -U --user keras_applications==1.0.6 --no-deps
pip3 install -U --user keras_preprocessing==1.0.5 --no-deps
apt-get install -y pkg-config zip g++ zlib1g-dev unzip python gcc-4.8 g++-4.8
cd /opt && 
    wget https://github.com/bazelbuild/bazel/releases/download/0.15.0/bazel-0.15.0-installer-linux-x86_64.sh && \
    chmod +x bazel-0.15.0-installer-linux-x86_64.sh && \
    ./bazel-0.15.0-installer-linux-x86_64.sh && \
    export PATH="$PATH:$HOME/bin" && \
    git clone https://github.com/tensorflow/tensorflow.git