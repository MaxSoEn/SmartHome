<h1>Smart Home</h1>
<br/><br/>
<p>
	This project is simple project for remote control with home from mobile or labtop depend on cayenne
	project has cam face detector and voice commands
</p>
<h2>requirements:</h2>

# install python and pip
	sudo apt install python3
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python3 get-pip.py
# if you see a problem try these commands and then try again
	sudo apt update
	sudo apt full-upgrade
	sudo apt install python3-pip
	sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 python3-dev -y
	sudo pip3 install --upgrade setuptools
	sudo reboot
# DHT11
	# Prepare the installation of CircuitPython libraries
		sudo pip3 install --upgrade adafruit-python-shell
		wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
		sudo python3 raspi-blinka.py
	# Install the CircuitPython-DHT Library
		sudo pip3 install adafruit-circuitpython-dht
		sudo apt-get install libgpiod2
# PCA for servo
	sudo pip3 install adafruit-circuitpython-pca9685
	sudo pip3 install adafruit-circuitpython-servokit
# for Cayenne
	git clone https://github.com/myDevicesIoT/Cayenne-MQTT-Python;cd Cayenne-MQTT-Python;python3 setup.py install;
# for camera
	# Install OpenCV with pip
		sudo pip3 install numpy
		sudo pip3 install opencv-contrib-python
	# if the above doesn't work try
		sudo pip3 install opencv-contrib-python==4.1.0.25
	# or
		sudo apt-get install python-opencv
# for voice
	sudo pip3 install SpeechRecognition pydub
	sudo pip3 install simpleaudio
	sudo pip3 install ffmpeg-python
	sudo pip3 install sounddevice
	sudo pip3 install scipy
	
	
<h2>TODO LIST</h2>

<ol>
	<li>Cayenne :</li>
	<ol type='a'>
		<li>Server:</li>
		<ol type='i'>
			<li>Heater</li>
			<li>Fan</li>
			<li>light(1 - 6)</li>
			<li>Motors(1, 2)</li>
		</ol>
		<li>Client:</li>
		<ol type='i'>
			<li>DHT11</li>
			<li>Flame</li>
			<li>UltraSonic(1 - 3)</li>
		</ol>
		<li>Notification:</li>
		<ol type='i'>
			<li>Front Door UltraSonic</li>
			<li>Flame</li>
		</ol>
	</ol>		
	<li>Commands:</li>
	<ol type='a'>
		<li>cam(face detector) open door (front)</li>
		<li>voice commands</li>
		<li>UltraSonic (2, 3) open door (2, 3)</li>
		<li>DHT11 (FAN, Heater)</li>
		<li>pir (1, 2, 3) open light (4, 5, 2)</li>
	</ol>
</ol>
<br/>

<table>
  <thead>
	<tr>
		<th>Name</th>
		<th>Pins</th>
		<th>GPIO</th>
		<th>CayenneName</th>
		<th>CayenneChannel</th>
		<th>Note</th>
	</tr>
  </thead>
  <tbody>
	<tr>
		<td>L1</td>
		<td>7</td>
		<td>4</td>
		<td>Light1</td>
		<td>0</td>
		<td>3rd Room</td>
	</tr>
	<tr>
		<td>L2</td>
		<td>11</td>
		<td>17</td>
		<td>Light2</td>
		<td>1</td>
		<td>2nd Room</td>
	</tr>
	<tr>
		<td>L3</td>
		<td>13</td>
		<td>27</td>
		<td>Light3</td>
		<td>2</td>
		<td>front Door</td>
	</tr>
	<tr>
		<td>L4</td>
		<td>15</td>
		<td>22</td>
		<td>Light4</td>
		<td>3</td>
		<td>1st Room</td>
	</tr>
	<tr>
		<td>L5</td>
		<td>23</td>
		<td>11</td>
		<td>Light5</td>
		<td>4</td>
		<td>4th Room</td>
	</tr>
	<tr>
		<td>T</td>
		<td>12</td>
		<td>18</td>
		<td>DHT11</td>
		<td>6</td>
		<td>Temperture</td>
	</tr>
	<tr>
		<td>u1</td>
		<td>38,36</td>
		<td>20,16</td>
		<td>UltraSonic1</td>
		<td>7</td>
		<td>echo,Trig</td>
	</tr>
	<tr>
		<td>u2</td>
		<td>19,21</td>
		<td>10,9</td>
		<td>UltraSonic2</td>
		<td>8</td>
		<td>echo,Trig</td>
	</tr>
	<tr>
		<td>u3</td>
		<td>24,26</td>
		<td>8,7</td>
		<td>UltraSonic3</td>
		<td>9</td>
		<td>echo,Trig</td>
	</tr>
	<tr>
		<td>flamePin,f</td>
		<td>32</td>
		<td>12</td>
		<td>Flame</td>
		<td>10</td>
		<td>Flame Detector</td>
	</tr>
	<tr>
		<td>m(0)</td>
		<td>29,31,33</td>
		<td>5,6,13</td>
		<td>WindowBlinds1</td>
		<td>11</td>
		<td>en1,in1,in2</td>
	</tr>
	<tr>
		<td>m(1)</td>
		<td>35,37,40</td>
		<td>19,26,21</td>
		<td>WindowBlinds2</td>
		<td>12</td>
		<td>in3,in4,en2</td>
	</tr>
	<tr>
		<td>cooler</td>
		<td>16</td>
		<td>23</td>
		<td>Fan</td>
		<td>13</td>
		<td>5v Fan</td>
	</tr>
	<tr>
		<td>heater</td>
		<td>18</td>
		<td>24</td>
		<td>Heater</td>
		<td>14</td>
		<td></td>
	</tr>
	<tr>
		<td>s</td>
		<td>3,5</td>
		<td>2,3</td>
		<td>Door(1-5)</td>
		<td>15,16,17,18,19</td>
		<td>SDA,SCL (4) is reversed</td>
	</tr>
	<tr>
		<td>p1,pi1</td>
		<td>8</td>
		<td>14</td>
		<td>PIR1</td>
		<td>20</td>
		<td>Motion Detection</td>
	</tr>
	<tr>
		<td>p2,pi2</td>
		<td>10</td>
		<td>15</td>
		<td>PIR2</td>
		<td>21</td>
		<td>Motion Detection</td>
	</tr>
	<tr>
		<td>p3,pi3</td>
		<td>22</td>
		<td>25</td>
		<td>PIR3</td>
		<td>22</td>
		<td>Motion Detection</td>
	</tr>
	<tr>
		<td>cam</td>
		<td>-</td>
		<td>-</td>
		<td>Cam</td>
		<td>23</td>
		<td>usb Camera for Face Detector</td>
	</tr>
	<tr>
		<td>voice</td>
		<td>-</td>
		<td>-</td>
		<td>Voice</td>
		<td>24</td>
		<td>usb mic for Voice Commands</td>
	</tr>
	<tr>
		<td>a</td>
		<td>-</td>
		<td>-</td>
		<td>Auto</td>
		<td>25</td>
		<td>Smart Auto</td>
	</tr>
  </tbody>
</table>

# screenShot
<img src="https://github.com/MaxSoEn/SmartHome/blob/main/Screenshot.jpg" >
