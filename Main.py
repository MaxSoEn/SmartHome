#!/usr/bin/env python

#Libraries
import cayenne.client
from Light import Relay
from DHT11 import Temp
from UltraSonic import Ultra
from sound import sound
import Drivers 
from RPi import GPIO
import logging
import time
import os
import cv2
import pickle
import numpy as np
from pygame import mixer
import speech_recognition as sr

# to make camera work in your face you need to train it first and change CamFiles

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "MQTT_USERNAME"
MQTT_PASSWORD  = "MQTT_PASSWORD"
MQTT_CLIENT_ID = "MQTT_CLIENT_ID"
MQTT_PORT = 1883

# Mode is for GPIO ONLY
GPIO.setmode(GPIO.BCM) #Enable GPIO

#PINS
p1 = 14     #pir1 8 GPIO 14
p2 = 15     #pir2 10 GPIO 15
p3 = 25     #pir3 22 GPIO 25

flamePin = 12           #32 GPIO 12
LightsPin = [4,         #7 GPIO 4
             17,        #11 GPIO 17
             27,        #13 GPIO 27
             22,        #15 GPIO 22
             11]	    #23 GPIO 11

tempPin = 18                #12 GPIO 18

UltraPin = [[20, 16],       #Trig,Echo -- 38,36 GPIO 20,16
            [10, 9],        #Trig,Echo -- 19,21 GPIO 10,9
            [8, 7]]         #Trig,Echo -- 26,24 GPIO 7,8

motorPin = [[5, 6, 13],     #en,in1,in2
            [21, 19, 26]]   #en,in1,in2

# Objects
l1 = Relay(LightsPin[0], 0.1, 0.1)
l2 = Relay(LightsPin[1], 0.1, 0.1)
l3 = Relay(LightsPin[2], 0.1, 0.1)
l4 = Relay(LightsPin[3], 0.1, 0.1)
l5 = Relay(LightsPin[4], 0.1, 0.1)

heater = Relay(24, 0.1, 0.1) #18 GPIO 24
cooler = Relay(23, 0.1, 0.1) #16 GPIO 23 

T = Temp(tempPin)

u1 = Ultra(UltraPin[0][0], UltraPin[0][1])
u2 = Ultra(UltraPin[1][0], UltraPin[1][1])
u3 = Ultra(UltraPin[2][0], UltraPin[2][1])

m = Drivers.l298(2, en1=motorPin[0][0], in1=motorPin[0][1], in2=motorPin[0][2], in3=motorPin[1][1], in4=motorPin[1][2], en2=motorPin[1][0]) #2 motors for Window Blinds

s = Drivers.PCA()       #SDA,SCL -- 3,5 GPIO 2,3


def callback(c):    #Flame Interupt
    f = GPIO.input(c)
    print("flame detected")
    client.virtualWrite(10, f,"Burn", "d")
#make Intrupt pin
GPIO.add_event_detect(flamePin, GPIO.BOTH, bouncetime=5)
GPIO.add_event_callback(flamePin, callback)  # assign function to GPIO PIN, Run Function


#====================main Setup=====================
voice = 0
a = 1
cam = 0
mixer.init()#voice initlization

m.stop(2)

GPIO.setup(flamePin, GPIO.IN)#flame Setup

GPIO.setup(p1, GPIO.IN)#PIR1 Setup
GPIO.setup(p2, GPIO.IN)#PIR2 Setup
GPIO.setup(p3, GPIO.IN)#PIR3 Setup

#turn of lights
l1.turnOff(False)
l2.turnOff(False)
l3.turnOff(False)
l4.turnOff(False)
L5.turnOff(False)

'''
#closing all doors
for i in range(5):
    if(i != 4):
        s.closeDoor(i, 1)
        print("Door ", i, " is closed")
    else:
        s.isOpen[4] = 1
        s.openDoor(i, 1)
        print("Door ", i, " is closed")
'''
s.isOpen[4] = 1

Temp_min = 25       #this is temperature minimum value
Temp_max = 27       #this is temperature maximum value

prev = [0, 0, 0, 0, 0, 0, #lights 0-5
        0,                #temp 6
        0, 0, 0,          #ultra 7-9
        0,                #flame 10
        0, 0,             #window 11,12
        0, 0,             #cooler,Heater 13,14
        0, 0, 0, 0, 0,    #doors 15-19
        0, 0, 0           #pir 20-22
        ]

#voices setup
files = []
for file in sorted(os.listdir( "voices/")):
    if(not(file.endswith(".mp3"))):
        continue
    if(os.path.isfile("voices/" + file)):
        files.append("voices/" + file)
print(files)

def playsound(n):
    mixer.music.load(files[n])
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.001)

#Camera Code:
video = cv2.VideoCapture(-1)
base = os.path.realpath("./")
cascade = cv2.CascadeClassifier(base +"/CamFiles/haarcascade_frontalface_default.xml")

recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read(base + "/CamFiles/trainner.yml")

labels = {}
with open("CamFiles/labels.pickle", 'rb') as f:
    og_label = pickle.load(f)
    labels = {v:k for k,v in og_label.items()}

d = time.time()

playsound(0)
vo = sound()

#Cayenne Recieve function
# The callback for when a message is received from Cayenne.
def on_message(message):
    global voice, cam, a
    # If there is an error processing the message return an error string, otherwise return nothing.
    #print("message received: " + str(message))
    print(message.channel," is call with value" ,message.value)

    if(message.channel == 0):   #Light1
        if(message.value == '1'):
            if(prev[0] != 1):
                prev[0] = 1
                print("Led 1 is on")
                l1.turnOn()
        else:
            if(prev[0] != 0):
                prev[0] = 0
                print("Led 1 is off")
                l1.turnOff()

    if(message.channel == 1):   #Light2
        if(message.value == '1'):
            if(prev[1] != 1):
                prev[1] = 1
                print("Led 2 is on")
                l2.turnOn()
        else:
            if(prev[1] != 0):
                prev[1] = 0
                print("Led 2 is off")
                l2.turnOff()

    if(message.channel == 2):   #light3
        if(message.value == '1'):
            if(prev[2] != 1):
                prev[2] = 1
                print("Led 3 is on")
                l3.turnOn()
        else:
            if(prev[2] != 0):
                prev[2] = 0
                print("Led 3 is off")
                l3.turnOff()

    if(message.channel == 3):   #light4
        if(message.value == '1'):
            if(prev[3] != 1):
                prev[3] = 1
                print("Led 4 is on")
                l4.turnOn()
        else:
            if(prev[3] != 0):
                prev[3] = 0
                print("Led 4 is off")
                l4.turnOff()

    if(message.channel == 4):   #Light5
        if(message.value == '1'):
            if(prev[4] != 1):
                prev[4] = 1
                print("Led 5 is on")
                l5.turnOn()
        else:
            if(prev[4] != 0):
                prev[4] = 0
                print("Led 5 is off")
                l5.turnOff()

    if(message.channel == 11):  #widow Blinds1
        if(message.value == '1'):
            if(prev[11] != 1):
                prev[11] = 1
                print("Window 1 is opening")
                m.openWindow(0, d=0.7)
        else:
            if(prev[11] != 0):
                prev[11] = 0
                print("Window 1 is closing")
                m.closeWindow(0, d=0.6)
    if(message.channel == 12):  #widow Blinds2
        if(message.value == '1'):
            if(prev[12] != 1):
                prev[12] = 1
                print("Window 2 is opening")
                m.openWindow(1, d=0.46)
        else:
            if(prev[12] != 0):
                prev[12] = 0
                print("Window 2 is closing")
                m.closeWindow(1, d=0.6)

    if(message.channel == 13):  #Fan
        if(message.value == '1'):
            if(prev[13] != 1):
                prev[13] = 1
                print("Fan Powered ON")
                cooler.turnOn()
        else:
            if(prev[13] != 0):
                prev[13] = 0
                print("Fan Powered OFF")
                cooler.turnOff()
            
    if(message.channel == 14):  #Heater
        if(message.value == '1'):
            if(prev[14] != 1):
                prev[14] = 1
                print("Heater Powered ON")
                heater.turnOn()
        else:
            if(prev[14] != 0):
                prev[14] = 0
                print("Heater Powered OFF")
                heater.turnOff()
                
    if(message.channel == 15):  #Door1
        if(message.value == '1'):
            if(prev[15] != 1):
                prev[15] = 1
                print("Door 1 is opening")
                s.closeDoor(4)
        else:
            if(prev[15] != 0):
                prev[15] = 0
                print("Door 1 is closing")
                s.openDoor(4)
    if(message.channel == 16):  #Door2
        if(message.value == '1'):
            if(prev[16] != 1):
                prev[16] = 1
                print("Door 2 is opening")
                s.openDoor(1)
        else:
            if(prev[16] != 0):
                prev[16] = 0
                print("Door 2 is closing")
                s.closeDoor(1)
    if(message.channel == 17):  #Door3
        if(message.value == '1'):
            if(prev[17] != 1):
                prev[17] = 1
                print("Door 3 is opening")
                s.openDoor(2)
        else:
            if(prev[17] != 0):
                prev[17] = 0
                print("Door 3 is closing")
                s.closeDoor(2)
    if(message.channel == 18):  #Door4    
        if(message.value == '1'):
            if(prev[18] != 1):
                prev[18] = 1
                print("Door 4 is opening")
                s.openDoor(3)
        else:
            if(prev[18] != 0):
                prev[18] = 0
                print("Door 4 is closing")
                s.closeDoor(3)
    if(message.channel == 19): #Front Door
        if(message.value == '1'):
            if(prev[19] != 1):
                prev[19] = 1
                print("Door Front is opening")
                s.openDoor(0)
        else:
            if(prev[19] != 0):
                prev[19] = 0
                print("Door Front is closing")
                s.closeDoor(0)

    if(message.channel == 23): #voice
        if(message.value == '1'):
            print("open voice")
            voice = 1
        else:
            print("close voice")
            voice = 0

    if(message.channel == 24): #cam
        if(message.value == '1'):
            print("open cam")
            cam = 1
        else:
            print("close cam")
            cam = 0

    if(message.channel == 25): #auto
        if(message.value == '1'):
            print("open auto")
            a = 1
        else:
            print("close auto")
            a = 0

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
# For a secure connection use port 8883 when calling client.begin:
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=MQTT_PORT, loglevel=logging.INFO)

timestamp = time.time()
try:
    while True:
        client.loop()
        while cam:
            client.loop()
            if(s.isOpen[0] == 0):
                d = time.time()
            elif(time.time() >= d + 3):
                prev[19] = 0
                s.closeDoor(0)
                client.virtualWrite(19, 0, "FrontDoor", "d")
            check,frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)

            for x,y,w,h in face:
                face_save = gray[y:y+h, x:x+w]

                ID, conf = recognise.predict(face_save)

                if conf >= 20 and conf <= 115:
                    print("conf:  {}".format(conf))
                    print(labels[ID])

                    # Checking the ID
                    if(labels[ID] == 'ashram' or labels[ID] == 'mostafa'):
                        prev[19] = 1
                        s.openDoor(0)
                        client.virtualWrite(19, 1,"FrontDoor", "d")
                    else:
                        prev[19] = 0
                        s.closeDoor(0)
                        client.virtualWrite(19, 0,"FrontDoor", "d")
                    #cv2.imwrite("Images/frame%d.jpg" % len(os.listdir("Images/"), frame)
                    cv2.putText(frame,labels[ID],(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX ,1, (0,0,255), 2, cv2.LINE_AA )

                frame = cv2.rectangle(frame, (x,y), (x+w,y+h),(255,103,45),4)

        if (time.time() > timestamp + 1.3):
            try:
                temp = T.getTemp()
                if(prev[6] != temp):
                    prev[6] = temp
                    client.celsiusWrite(6, temp)
                if(temp < Temp_min):
                    if(prev[14] != 1 and voice == 0 and a == 1):
                        prev[14] = 1
                        heater.turnOn()
                        client.virtualWrite(14, 1,"Heater", "d")
                elif(temp <= Temp_max and temp >= Temp_min):
                    if(prev[13] != 0 and voice == 0 and a == 1):
                        prev[13] = 0
                        cooler.turnOff()
                        client.virtualWrite(13, 0,"Fan", "d")
                    if(prev[14] != 0 and voice == 0):
                        prev[14] = 0
                        heater.turnOff()
                        client.virtualWrite(14, 0,"Heater", "d")
                    print("Temperture is %d be Carefully" %T.temp)
                else:
                    if(prev[13] != 1 and voice == 0 and a == 1):
                        prev[13] = 1
                        cooler.turnOn()
                        client.virtualWrite(13, 1,"Fan", "d")
            except RuntimeError as error:
                print(error.args[0])
                continue
            except:
                print("Error")
            
            if(u1.calcDist() <= 20):
                #print("distance is", u1.calcDist())
                if(prev[7] != 1):
                    prev[7] = 1
                    client.virtualWrite(7, 1,"Motion", "d")
            else:
                if(prev[7] != 0):
                    prev[7] = 0
                    client.virtualWrite(7, 0,"Motion", "d")
            if(u2.calcDist() <= 20):
                if(prev[8] != 1):
                    prev[8] = 1
                    client.virtualWrite(8, 1,"Motion", "d")
                    #if(prev[16] != 1):
                    #    prev[16] = 1
                    #    s.openDoor(1)
                    #    client.virtualWrite(16, 1,"Door2", "d")
            else:
                if(prev[8] != 0):
                    prev[8] = 0
                    client.virtualWrite(8, 0,"Motion", "d")
                    #if(prev[16] != 0):
                    #    prev[16] = 0
                    #    s.closeDoor(1)
                    #    client.virtualWrite(16, 0,"Door2", "d")
            if(u3.calcDist() <= 20):
                if(prev[9] != 1):
                    prev[9] = 1
                    client.virtualWrite(9, 1,"Motion", "d")
                    #if(prev[18] != 1):
                    #    prev[18] = 1
                    #    print("Door 4 is opening")
                    #   s.openDoor(3)
                    #   client.virtualWrite(18, 1,"Door4", "d")
            else:
                if(prev[9] != 0):
                    prev[9] = 0
                    client.virtualWrite(9, 0, "Motion", "d")
                    #if(prev[18] != 0):
                    #    prev[18] = 0
                    #    print("Door 4 is closing")
                    #    s.closeDoor(3)
                    #    client.virtualWrite(18, 0,"Door4", "d")
            f = GPIO.input(flamePin)
            if(prev[10] != f):
                prev[10] = f
                client.virtualWrite(10, f, "Burn", "d")
            pi1 = GPIO.input(p1)
            if(prev[20] != pi1):
                prev[20] = pi1
                client.virtualWrite(20, pi1, "PIR1", "d")
                if(voice == 0 and a == 1):
                    if(pi1):
                        l4.turnOn()
                    else:
                        l4.turnOff()
            pi2 = GPIO.input(p2)
            if(prev[21] != pi2):
                prev[21] = pi2
                client.virtualWrite(21, pi2, "PIR2", "d")
                if(voice == 0 and a == 1):
                    if(pi2):
                        l5.turnOn()
                    else:
                        l5.turnOff()
            pi3 = GPIO.input(p3)
            if(prev[22] != pi3):
                prev[22] = pi3
                client.virtualWrite(22, pi3, "PIR3", "d")
                if(voice == 0 and a == 1):
                    if(pi3):
                        l2.turnOn()
                    else:
                        l2.turnOff()
            timestamp = time.time()
        if(voice == 1):
            client.loop()
            playsound(1)
            vo.record(4)
            text = ''
            try:
                text = vo.getText()
                text = text.lower().replace('live', 'light').replace('oven','open').replace('like','light').replace('the', '').replace('-', ' ').replace('closed', 'close').replace('darwin', 'door one').replace('on', 'one').replace('play bubble', 'open').replace('stop','').replace('onee','one').replace('bank', 'one').replace('play store','front door').replace('dor', 'door').replace('fronet', 'front').replace('blues','close').replace('doors','door').replace('lights','light')
                text = text.replace('from today', 'front door').replace('owen','open').replace('sale', 'fan').replace('fin', 'fan').replace('fen', 'fan').replace('finn','fan')
                text = text.replace('train','fan').replace('play','close').replace('shazam','fan').replace('urban','open').replace('friend','fan').replace('fern','fan').replace('closest','close').replace('10','fan').replace('ten','fan').replace('phone','fan').replace('open one', 'open door one').replace('  ',' ').strip()
                print(text)
            except sr.UnknownValueError:
                print("Voice ERROR")
            '''
            finally:
                print(time.time() - t)
            '''
            if(text.__contains__("open light one") or text.__contains__("open light 1")):
                playsound(3)
                prev[0] = 1
                l1.turnOn()
            elif(text.__contains__("open light two") or text.__contains__("open light 2") or text.__contains__("open light to") or text.__contains__("open light too")):
                playsound(3)
                prev[1] = 1
                l2.turnOn()
            elif(text.__contains__("close light one") or text.__contains__("close light 1")):
                playsound(3)
                prev[0] = 0
                l1.turnOff()
            elif(text.__contains__("close light two") or text.__contains__("close light 2") or text.__contains__("close light to") or text.__contains__("close light too")):
                playsound(3)
                prev[1] = 0
                l2.turnOff()
            elif(text.__contains__("open front door")):
                playsound(3)
                prev[19] = 1
                s.openDoor(0)
            elif(text.__contains__("open door one") or text.__contains__("open door 1")):
                playsound(3)
                prev[15] = 1
                s.closeDoor(4)
            elif(text.__contains__("close door one") or text.__contains__("close door 1")):
                playsound(3)
                prev[15] = 0
                s.openDoor(4)
            elif(text.__contains__("close front door")):
                playsound(3)
                prev[19] = 0
                s.closeDoor(0)
            elif(text.__contains__("open fan")):
                playsound(3)
                prev[13] = 1
                cooler.turnOn()
            elif(text.__contains__("close fan")):
                playsound(3)
                prev[13] = 0
                cooler.turnOff()
            elif(text.__contains__("open heater")):
                playsound(3)
                prev[14] = 1
                heater.turnOn()
            elif(text.__contains__("close heater")):
                playsound(3)
                prev[14] = 0
                heater.turnOff()
            elif(text.__contains__("open door two") or text.__contains__("open door 2") or text.__contains__("open door to") or text.__contains__("open door too")):
                playsound(3)
                prev[16] = 1
                s.closeDoor(1)
            elif(text.__contains__("close door two") or text.__contains__("close door 2") or text.__contains__("close door to") or text.__contains__("close door too")):
                playsound(3)
                prev[16] = 0
                s.openDoor(1)
            else:
                with open("errors2.txt", 'a') as f:
                    f.write("<" + text + ">\n")
                playsound(4)
except KeyboardInterrupt:
    print("Program Closed By User")
finally:
    video.release()
    cv2.destroyAllWindows()
    #closing all doors
    for i in range(5):
        if(i != 4):
            if(s.isOpen[i] != 0):
                s.closeDoor(i)
                print("Door ", i, " is closed")
        else:
            if(s.isOpen[i] != 1):
                s.openDoor(i)
                print("Door ", i, " is closed")
    GPIO.remove_event_detect(c)
    GPIO.cleanup()
    
