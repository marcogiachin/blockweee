# -*- coding: utf-8 -*-
import json
import sys   
import os       
import time
import datetime
import SDL_Pi_HDC1080
import MPU_6050
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BCM)
#ON_PIN = 18
LED_PIN = 17

 
GPIO.setup(LED_PIN, GPIO.OUT)
#GPIO.setup(ON_PIN, GPIO.OUT)
#GPIO.output(ON_PIN, True)

print (" Reading Data of Gyroscope, Accelerometer, Temperature and Humidity")

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
mpu6050 = MPU_6050.MPU_6050()

time.sleep(2)

try:
    while True:
        GPIO.setwarnings(False)
        #Reading value of temperature and humidity
        temp = hdc1080.readTemperature()
        time.sleep(1)
        hum = hdc1080.readHumidity()
        print("-----------------")
        d = datetime.datetime.now()
        
        if d.hour == 23:
            h = 0
        else:
            h = d.hour+1
        
        print("Date and time: %s" %d.replace(hour=h).strftime("%c")) 
        print("Temperature = %3.1f C" % temp)
        print("Humidity = %3.1f %%" % hum)
        print("")
        
        #Reading value of accelerometer and gyroscope
        Ax, Ay, Az = mpu6050.read_acc()
        Gx, Gy, Gz = mpu6050.read_gyro()
        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)     
        print("-----------------")
        #Preparing the tx for the BCs
        obj={
            "data" : {
                "temperature" : '%.2f'%temp,
                "humidity" : '%.2f'%hum,
                "acceleration" : '%.2f'%Az,
                "rotation" : '%.2f'%Gz,
                "id" : "427832FFFFFF9865FFFFFF81",
                'date' : d.replace(hour = h).strftime("%c"),
                'time' : int(round(time.time() * 1000))
            },
            "public_key" : "5ba98d071bb7fe9abcd9e7e3b1bf2d5664d7c87b41929c1b82f5765ae6e7bf82"
        }
        GPIO.output(LED_PIN, True)
        url = 'http://172.20.10.2:3000/api/send_tx' #Address of the function on the api server
        headers = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
        r = requests.post(url, data=json.dumps(obj), headers=headers)
        time.sleep(5)
        GPIO.output(LED_PIN, False)
        time.sleep(60)

except:
    #os.system("python3 read_data.py")
    GPIO.output(LED_PIN, False)
    GPIO.cleanup()

