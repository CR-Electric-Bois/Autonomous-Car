from MotorModule import Motor
#import KeyPressModule as kp
#from CameraModule import piCam
import JoystickModule as js
from time import sleep

#################################
motor = Motor(25, 24, 23, 20, 16, 12) #GPIO pins of both motor
movement = 'Joystick' #Option of use Keybord, ['Keyboard', 'Joystick']
#################################


def main():
    if movement == 'Joystick':
        #print(js.getJS())
        #sleep(0.05)
        jsVal = js.getJS()
        motor.move(-(jsVal['axis2']), jsVal['axis1'], 0.1)
    else:
        motor.move(0.5, -1, 2) #Negative values for speed is backward and for turn is left
        motor.stop(2)
        motor.move(-0.5, 1, 2)
        motor.stop(2)

if __name__ == '__main__':
    while True:
        main()