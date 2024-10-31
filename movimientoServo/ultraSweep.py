#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicServoControl.py
# Description : Activate servo when ultrasonic sensor detects an object
# Author      : www.freenove.com (combined and modified by ChatGPT)
# Modification: 2023/10/15
########################################################################

import os
os.system("sudo pigpiod")
from gpiozero import AngularServo, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Configuración de la fábrica de pines
my_factory = PiGPIOFactory()

# Configuración del servomotor
myGPIO = 18
SERVO_DELAY_SEC = 0.001
myCorrection = 0.0
maxPW = (2.5 + myCorrection) / 1000
minPW = (0.5 - myCorrection) / 1000
servo = AngularServo(myGPIO, initial_angle=0, min_angle=0, max_angle=180,
                     min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=my_factory)

# Configuración del sensor ultrasónico
trigPin = 23
echoPin = 24
sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=3, pin_factory=my_factory)

def move_servo():
    """Función para hacer que el servomotor realice un barrido completo de 0 a 180 grados y viceversa."""
    for angle in range(0, 181, 1):  # Rota de 0 a 180 grados
        servo.angle = angle
        time.sleep(SERVO_DELAY_SEC)
    time.sleep(0.5)
    for angle in range(180, -1, -1):  # Rota de 180 a 0 grados
        servo.angle = angle
        time.sleep(SERVO_DELAY_SEC)
    time.sleep(0.5)

def loop():
    """Bucle principal que activa el servomotor si se detecta un objeto a menos de 50 cm."""
    while True:
        distance = sensor.distance * 100  # Convertir la distancia a cm
        print('Distance: {:.2f} cm'.format(distance))
        
        if distance < 50:  # Umbral para activar el servomotor
            print("Object detected within 50 cm! Activating servo...")
            move_servo()
        else:
            print("No object within 50 cm.")
        
        time.sleep(1)

if __name__ == '__main__':
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        # Cerrar recursos al final del programa
        servo.close()
        sensor.close()
        os.system("sudo killall pigpiod")
        print("Ending program")
