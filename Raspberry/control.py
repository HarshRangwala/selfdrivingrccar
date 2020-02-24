from flask import Flask, jsonify, request, Response
import RPi.GPIO as GPIO
import time
import json
import configuration

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BACK_MOTOR_DATA_ONE = configuration.BACK_MOTOR_DATA_ONE
BACK_MOTOR_DATA_TWO = configuration.BACK_MOTOR_DATA_TWO
BACK_MOTOR_ENABLE_PIN = configuration.BACK_MOTOR_ENABLE_PIN
FRONT_MOTOR_DATA_ONE = configuration.FRONT_MOTOR_DATA_ONE
FRONT_MOTOR_DATA_TWO = configuration.FRONT_MOTOR_DATA_TWO
PWM_FREQUENCY = configuration.PWM_FREQUENCY

GPIO.setup(BACK_MOTOR_DATA_ONE,GPIO.OUT)
GPIO.setup(BACK_MOTOR_DATA_TWO,GPIO.OUT)
GPIO.setup(FRONT_MOTOR_DATA_ONE,GPIO.OUT)
GPIO.setup(FRONT_MOTOR_DATA_TWO,GPIO.OUT)


GPIO.output(BACK_MOTOR_DATA_ONE,GPIO.LOW)
GPIO.output(BACK_MOTOR_DATA_TWO,GPIO.LOW)
GPIO.output(FRONT_MOTOR_DATA_ONE,GPIO.LOW)
GPIO.output(FRONT_MOTOR_DATA_TWO,GPIO.LOW)

'''
app = Flask(__name__) Special var in python that is just the name of the module. This helps Flask to know
                      where to look for template and static files. 
                        
'''
app = Flask(__name__)                 
@app.route('/messages', methods = ['POST']) # rout are used for the webpage to have additional functionality.
def api_message():
        data = request.args.get('data')
        control(data)

def control(key):
        print(key)
        if key == 's': 
                print ("Backward")
                GPIO.output(BACK_MOTOR_DATA_ONE, False)
                GPIO.output(BACK_MOTOR_DATA_TWO, True)
                            
        elif key == 'w':
                print ("forward")
                GPIO.output(BACK_MOTOR_DATA_ONE, True)
                GPIO.output(BACK_MOTOR_DATA_TWO, False)

        elif key == 'a':
                print ("Left")
                GPIO.output(FRONT_MOTOR_DATA_ONE, False)
                GPIO.output(FRONT_MOTOR_DATA_TWO, True)
        elif key == 'd':
                print ("Right")
                GPIO.output(FRONT_MOTOR_DATA_ONE, True)
                GPIO.output(FRONT_MOTOR_DATA_TWO, False)
        elif key == 'e':
                print ("Forward Left")
                GPIO.output(FRONT_MOTOR_DATA_ONE, True)
                GPIO.output(BACK_MOTOR_DATA_ONE, True)
        elif key == 'q':
                print ("Forward Right")
                GPIO.output(FRONT_MOTOR_DATA_TWO, True)
                GPIO.output(BACK_MOTOR_DATA_ONE, True)
                
        elif key == 'x':
                GPIO.output(BACK_MOTOR_DATA_ONE,GPIO.LOW)
                GPIO.output(BACK_MOTOR_DATA_TWO,GPIO.LOW)
                GPIO.output(FRONT_MOTOR_DATA_ONE,GPIO.LOW)
                GPIO.output(FRONT_MOTOR_DATA_TWO,GPIO.LOW)
        elif key == 'quit':
                quit()

if __name__ == '__main__':
    #Home hotspot ip: 192.168.43.137
    app.run(host='192.168.0.31', port=5000, debug=False) #debug = True
