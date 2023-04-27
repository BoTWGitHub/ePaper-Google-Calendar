#update system
sudo apt-get update
sudo apt-get upgrade

#get e-paper display requirement
sudo apt-get pip
pip install pillow
pip install numpy
pip install RPi.GPIO
pip install spidev

#ics requirement
pip install ics
pip install arrow
pip install requests

#make config file
mkdir config
echo > config/calUrls.cfg
echo > config/weatherConfig.json
