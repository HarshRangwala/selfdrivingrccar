# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:25:28 2020

@author: Anuj
"""

import configuration
import RPi.GPIO as GPIO
from time import sleep
import socket

host = "192.168.0.19"
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
message  = "START"
client_socket.send(message.encode())

BACK_MOTOR_DATA_ONE = configuration.BACK_MOTOR_DATA_ONE
BACK_MOTOR_DATA_TWO = configuration.BACK_MOTOR_DATA_TWO
BACK_MOTOR_ENABLE_PIN = configuration.BACK_MOTOR_ENABLE_PIN
FRONT_MOTOR_DATA_ONE = configuration.FRONT_MOTOR_DATA_ONE
FRONT_MOTOR_DATA_TWO = configuration.FRONT_MOTOR_DATA_TWO
PWM_FREQUENCY = configuration.PWM_FREQUENCY
INITIAL_PWM_DUTY_CYCLE = configuration.INITIAL_PWM_DUTY_CYCLE

GPIO.setwarnings(False)
#GPIO setip
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK_MOTOR_DATA_ONE, GPIO.OUT)
GPIO.setup(BACK_MOTOR_DATA_TWO, GPIO.OUT)
GPIO.setup(FRONT_MOTOR_DATA_ONE, GPIO.OUT)
GPIO.setup(FRONT_MOTOR_DATA_TWO, GPIO.OUT)
GPIO.setup(BACK_MOTOR_ENABLE_PIN, GPIO.OUT)


def set_right_mode():
    """Set mode to Right"""
    client_socket.send('RIGHT'.encode())
    GPIO.output(FRONT_MOTOR_DATA_ONE, True)
    GPIO.output(FRONT_MOTOR_DATA_TWO, False)

def set_left_mode():
    """Set mode to Left"""
    client_socket.send('LEFT'.encode())
    GPIO.output(FRONT_MOTOR_DATA_ONE, False)
    GPIO.output(FRONT_MOTOR_DATA_TWO, True)

def set_reverse_mode():
    """Set mode to Reverse"""
    client_socket.send('REVERSE'.encode())
    GPIO.output(BACK_MOTOR_DATA_ONE, False)
    GPIO.output(BACK_MOTOR_DATA_TWO, True)

def set_forward_mode():
    """Set mode to Forward"""
    client_socket.send('FORWARD'.encode())
    GPIO.output(BACK_MOTOR_DATA_ONE, True)
    GPIO.output(BACK_MOTOR_DATA_TWO, False)

def set_stop_mode():
    client_socket.send('STOP'.encode())
    GPIO.output(BACK_MOTOR_DATA_ONE, False)
    GPIO.output(BACK_MOTOR_DATA_ONE, False)

def set_forward_right_mode():
    client_socket.send('FORWARD RIGHT'.encode())
    GPIO.output(FRONT_MOTOR_DATA_ONE, True)
    GPIO.output(FRONT_MOTOR_DATA_TWO, False)
    GPIO.output(BACK_MOTOR_DATA_ONE, True)
    GPIO.output(BACK_MOTOR_DATA_TWO, False)

def set_forward_left_mode():
    client_socket.send('FORWARD LEFT'.encode())
    GPIO.output(FRONT_MOTOR_DATA_ONE, False)
    GPIO.output(FRONT_MOTOR_DATA_TWO, True)
    GPIO.output(BACK_MOTOR_DATA_ONE, True)
    GPIO.output(BACK_MOTOR_DATA_TWO, False)

while message.lower().strip() != 'bye':
    command = client_socket.recv(1024).decode()
    
    if command == '0':
        print("Recieved from server: STOP")
        set_stop_mode()
    if command == '1':
        print("Recieved from server: FORWARD")
        set_forward_mode()
    if command == '2':
        print("Recieved from server: REVERSE")
        set_reverse_mode()
    if command == '3':
        print("Recieved from server: RIGHT")
        set_right_mode()
    if command == '4':
        print("Recieved from server: LEFT")
        set_left_mode()
    if command == '5':
        print("Recieved from server: FORWARD RIGHT")
        set_forward_right_mode()
    if command == '5':
        print("Recieved from server: FORWARD RIGHT")
        set_forward_left_mode()
    else:
        print("INVALID USER INPUT")
client_socket.close()
