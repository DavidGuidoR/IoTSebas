#!/usr/bin/env python3
########################################################################
# Filename    : SenseLED.py
# Description : Control led with infrared Motion sensor.
# auther      : www.freenove.com
# modification: 2023/05/11
########################################################################
from gpiozero import LED,MotionSensor
import time

ledPin = 18       # define ledPin
ledPin2 = 25

sensorPin = 17    # define sensorPin
led    = LED(ledPin)     
led2    = LED(ledPin2)  
sensor = MotionSensor(sensorPin)
sensor.wait_for_no_motion()
def loop():
    # Variables to hold the current and last states
    currentstate = False
    previousstate = False
    while True:
        # Read sensor state
        currentstate = sensor.motion_detected
        # If the sensor is triggered
        if currentstate == True and previousstate == False:
            led.on()
            led2.off()
            print("Motion detected!led turned on >>>")
            
            # Record previous state
            previousstate = True
        # If the sensor has returned to ready state
        elif currentstate == False and previousstate == True:
            led.off()
            led2.on()
            print("No Motion!led turned off <<")
            previousstate = False
        # Wait for 10 milliseconds
        time.sleep(0.01)

def destroy():
    led.close() 
    sensor.close()                     

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        print("Ending program")