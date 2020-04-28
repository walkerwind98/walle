#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

import time 
import urequests
import utime
import ujson
import ubinascii

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



gyroright = GyroSensor(Port.S1)
gyroleft = GyroSensor(Port.S3)

gyroright.reset_angle(0)
gyroleft.reset_angle(0)


touch1 = TouchSensor(Port.S2)
touch2 = TouchSensor(Port.S4)

print('Waiting for Right Touch Input to Start')
while(touch1.pressed() is False):
     wait(50)

#Pairing for bluetooth, must pair the devices ebeforehand but not connect
server = BluetoothMailboxServer()
mbox = TextMailbox('greeting',server)

print('waiting for connection ...')
server.wait_for_connection()
print('connected!')
wait(1000)
#mbox.send('Start') #This is the line that sends a string to the other ev3


angleleft = 0
angleright = 0 
anglespeedleft = 0
anglespeedright = 0
deltatime = 0

touchleft = False
touchright = False
f = open('controller1.csv', "a+")
#data = DataLog('time','angleright','angleleft','anglespeedright','anglespeedleft')

starttime = time.time()
while(True):

     touchright = touch1.pressed()
     touchleft = touch2.pressed()
     if(touchright is True and touchleft is True):
          gyroright.reset_angle(0)
          gyroleft.reset_angle(0)
     angleright = gyroright.angle()
     angleleft = gyroleft.angle()
     wait(100)
     if(angleright < 5 and angleright > -5):
          angleright = 0
     if(angleleft < 5 and angleleft > -5):
          angleleft = 0

     
     
     mbox.send(str(deltatime) + " " + str(angleright)+" "+str(angleleft))
     print(str(deltatime) + " " + str(angleright)+" "+str(angleleft))
     currenttime = time.time()
     deltatime = currenttime-starttime


     f.write(str(deltatime) + ','+ str(angleright) +","+ str(angleleft) + "," + str(anglespeedright) + "," + str(anglespeedleft))
     #print("Processing Time: ", deltatime)
     #print("Touch Left: ",touchleft)
     #print("Touch Right:gyro ",touchright)
     print("Angle Left: ", angleleft)
     print("Angle Right: ", angleright)
     #print("Angular Speed Left: ", anglespeedleft)
     #print("Angular Speed Right: ", anglespeedright)
     
f.close()
    





