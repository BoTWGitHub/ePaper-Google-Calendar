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

echo '===> install i2c-tools'
sudo apt-get install i2c-tools

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
echo '===> install vim'
sudo apt-get install vim

#make config file
echo '===> make config folder and file'
mkdir config
echo > config/calUrls.cfg
echo > config/weatherConfig.json

echo '===> adjust script mod'
sudo chmod +x ~/ePaper-Google-Calendar/ePaperCalendar/updateThenShutdown.sh

echo '===> copy service script to system'
sudo cp ~/ePaper-Google-Calendar/ePaperCalendar/Calendar.service /etc/systemd/system/Calendar.service

echo '===> install pisugar server'
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash

echo '===> remember to enable SPI and I2C'
sudo raspi-config

#echo '===> start Calendar service'
#sudo systemctl daemon-reload
#sudo systemctl enable Calendar.service

#sudo reboot
