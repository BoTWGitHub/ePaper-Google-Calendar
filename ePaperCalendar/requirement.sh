#update system
echo '===> update the system'
sudo apt-get update
sudo apt-get upgrade

#get e-paper display requirement
echo '===> install python3-pip'
sudo apt-get install python3-pip

echo '===> install python3-pil'
sudo apt-get install python3-pil

echo '===> install python3-numpy'
sudo apt-get install python3-numpy

echo '===> install RPi.GPIO'
sudo pip3 install RPi.GPIO

echo '===> install spidev'
sudo pip3 install spidev

#ics requirement
echo '===> install ics'
pip install ics
echo '===> install arrow'
pip install arrow
echo '===> install requests'
pip install requests

#make config file
echo '===> make config folder and file'
mkdir config
echo > config/calUrls.cfg
echo > config/weatherConfig.json
