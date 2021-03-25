import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT) #Output pin
pwm = GPIO.PWM(17, 50) #PWM to Pin 17 with a 50Hz pulse

pwm.start(0) #Doesn't set any angles on setup
duty = 2

while True:
    while duty <= 12:
        pwm.ChangeDutyCycle(duty)
        sleep(0.3)
        pwm.ChangeDutyCycle(0)
        sleep(0.7)
        duty = duty + 1

    sleep(2)
    pwm.ChangeDutyCycle(7)
    sleep(2)
    pwm.ChangeDutyCycle(2)
    sleep(2)
    duty = 2