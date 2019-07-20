#/bin/bash
sudo apt-get -y install autoconf build-essential libglib2.0-dev libssl-dev libcurl4-openssl-dev asciidoc
if [ ! -d "$DIRECTORY" ]; then
	git clone git://megous.com/megatools
fi
cd megatools && \
make -C docs && \ 
./autogen.sh && \
make && \
sudo make install 
rm -rf megatools
