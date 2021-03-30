'''
The idea of the module is to use the motors from the car using a 
L298N Motor Controller. This car has only 2 motors, one for steering and
a second one for speed.
The code only used the GPIO Pins
The function receives the speed and turn for the motors
Speed and turn are normalized from -1 to 1.
Delay is in seconds
'''

import RPi.GPIO as GPIO #Import GPIO
from time import sleep #Import Sleep

GPIO.setmode(GPIO.BCM) #Set the GPIO mode
GPIO.setwarnings(False) #No warnings

class Motor():
    def __init__(self, Motor1Enable, Motor1A, Motor1B, Motor2Enable, Motor2A, Motor2B):
        self.Motor1Enable = Motor1Enable #GPIO Motor pins
        self.Motor1A = Motor1A
        self.Motor1B = Motor1B
        self.Motor2Enable = Motor2Enable
        self.Motor2A = Motor2A
        self.Motor2B = Motor2B
        #Set up defined GPIO pins for Motor 1
        GPIO.setup(self.Motor1A, GPIO.OUT)
        GPIO.setup(self.Motor1B, GPIO.OUT)
        GPIO.setup(self.Motor1Enable, GPIO.OUT)
        #Set up defined GPIO pins for Motor 2
        GPIO.setup(self.Motor2A, GPIO.OUT)
        GPIO.setup(self.Motor2B, GPIO.OUT)
        GPIO.setup(self.Motor2Enable, GPIO.OUT)
        #Duty Cycle
        self.pwm1 = GPIO.PWM(self.Motor1Enable, 100) #100 frequency
        self.pwm1.start(0) #Duty Cycle
        self.pwm2 = GPIO.PWM(self.Motor2Enable, 100) #100 frequency
        self.pwm2.start(0) #Duty Cycle

    def move(self, speed = 0.5, turn = 0, t = 0):
        speed *= 100 #We normalized the speed from 0 to 1
        turn *= 100 #Normalized the turn

        if speed > 0: #Forward
            GPIO.output(self.Motor1A, GPIO.HIGH)
            GPIO.output(self.Motor1B, GPIO.LOW)
            self.pwm1.ChangeDutyCycle(abs(speed)) #Speed
            sleep(t) #Delay
            if turn > 0: #Right turn
                GPIO.output(self.Motor2A, GPIO.LOW)
                GPIO.output(self.Motor2B, GPIO.HIGH)
                self.pwm2.ChangeDutyCycle(abs(turn)) #How much angle on the turn
                sleep(t) #Delay
            else: #Turn left
                GPIO.output(self.Motor2A, GPIO.HIGH)
                GPIO.output(self.Motor2B, GPIO.LOW)
                self.pwm2.ChangeDutyCycle(abs(turn)) #How much angle on the turn
                sleep(t) #Delay
        else: #Backward
            GPIO.output(self.Motor1A, GPIO.LOW)
            GPIO.output(self.Motor1B, GPIO.HIGH)
            self.pwm1.ChangeDutyCycle(abs(speed)) #Speed
            sleep(t) #Delay
            if turn > 0: #Turn right
                GPIO.output(self.Motor2A, GPIO.LOW)
                GPIO.output(self.Motor2B, GPIO.HIGH)
                self.pwm2.ChangeDutyCycle(abs(turn)) #How much angle on the turn
                sleep(t) #Delay
            else: #Turn left
                GPIO.output(self.Motor2A, GPIO.HIGH)
                GPIO.output(self.Motor2B, GPIO.LOW)
                self.pwm2.ChangeDutyCycle(abs(turn)) #How much angle on the turn
                sleep(t) #Delay
    def stop(self, t = 0):
        self.pwm1.ChangeDutyCycle(0) #Stop
        self.pwm2.ChangeDutyCycle(0) #No turn
        sleep(t) #Delay

def main():
    motor.move(0.5, -1, 2) #Negative values for speed is backward and for turn is left
    motor.stop(2)
    motor.move(-0.5, 1, 2)
    motor.stop(2)

if __name__ == '__main__':
    motor = Motor(25, 24, 23, 20, 16, 12) #GPIO pins of both motor
    main()
