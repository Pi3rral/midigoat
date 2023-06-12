# esp-idf download and build
git clone -b v4.4 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
git submodule update --init --recursive
./install.sh
source export.sh
cd ..
