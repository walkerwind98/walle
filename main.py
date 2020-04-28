#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

import time
import urequests
import utime
import ujson
import ubinascii
import math

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()


Key = 'X2OxHa5uX5Tls6yttSOgLcOFh62H_7HKZayHGAcLYE'

def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
          #print(reply)
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)

#open file
file = open('driver1.csv','a+')
file.write(" First Line")

#Initialize Motors

MotorR = Motor(Port.D)
MotorL = Motor(Port.A)
touch = TouchSensor(Port.S1)

anglespdright=0
anglespdleft=0
motorspdright = 0
motorspdleft = 0
angles = ''

print('Waiting for Touch Input to Start')
while(touch.pressed() is False):
     wait(50)

SERVER = 'ev3dev'
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)



print('establishing connection...')
client.connect(SERVER)
print('connected!')
wait(1000)
#mbox.send('hello!')
#print(mbox.read())

anglestring = ''
angles = ''
t = 0
tprev = 0
prevangleright=0
prevangleleft=0

while(True):
     anglestring = mbox.read()

     anglestring = str(anglestring)
     #print("string is ",anglestring)

     if len(anglestring.split()) is 1 :
          anglestring = "0 0 0"


     angles = anglestring.split()
     #print("angles are",angles)
     t = round(float(angles[0]),3)
     #print(t)
     angleright = int(angles[1])
     angleleft = int(angles[2])
     

     maxspd=400

     #controller for speed
     
     motorspdright = maxspd*((angleright-90)/90 + 1)

     motorspdleft = maxspd*((angleleft-90)/90 + 1)
     
     if(motorspdright > maxspd):
          motorspdright = maxspd
     if(motorspdright <-maxspd):
          motorspdright = -maxspd
     if(motorspdleft > maxspd):
          motorspdleft=maxspd
     if(motorspdleft < -maxspd):
          motorspdleft=-maxspd

     print("right ",motorspdright)
     print("left ",motorspdleft)

     if(t is not tprev):
          file.write(str(t)+","+str(angleright)+","+str(angleleft) + ","+str(motorspdright)+","+str(motorspdleft)+"\n")
     #a
     tprev=t
     prevangleright = angleright
     prevangleleft = angleleft

     #Write to Motors
     MotorR.run(-motorspdright)
     MotorL.run(motorspdleft)

   
file.close()
    
    