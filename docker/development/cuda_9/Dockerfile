FROM mipo57/cuda9
RUN apt-get update && \
    apt-get install -y wget \  
                       gnupg2 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install tensorflow-gpu && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \ 
    git \ 
    openjdk-8-jre \ 
    libxrender1 \ 
    libxtst6 \
    python3-numba \
    python3-flask \
    python3-requests \
    python3-opencv \
    megatools \
    unzip

RUN cd /opt && \
    wget https://download.jetbrains.com/python/pycharm-community-2019.1.2.tar.gz && \
    tar -xzf pycharm-community-2019.1.2.tar.gz && \
    rm pycharm-community-2019.1.2.tar.gz && \
    ln -s /opt/pycharm-community-2019.1.2/bin/pycharm.sh /usr/bin/pycharm
COPY prepare_tf_build.sh /opt/prepare_tf_build.sh
RUN cd /opt && ./prepare_tf_build.sh