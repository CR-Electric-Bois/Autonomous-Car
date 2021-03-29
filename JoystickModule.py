'''
The idea of this module is to obtain the values from a controller
We use a PS4 controller connected via bluetooth
The values are stored in a dictionary and show in realtime
'''
import pygame #Detect key strokes
from time import sleep #Sleep is for the delays

pygame.init() #Initialize pygame
controller = pygame.joystick.Joystick(0) #Only one controller
controller.init()

#Dictionary for buttons and the axis of the joysticks, so everything is together
buttons = {'x':0, 'o':0, 't':0,'s':0,
            'L1':0, 'R1':0, 'L2':0, 'R2':0,
            'share':0, 'option':0,
            'axis1':0., 'axis2':0., 'axis3':0., 'axis4':0.} #0 is not pressed and 1 pressed. Axis are float and range from -1 to 1
#4 axis because each joystick can go up or down, and right or left
axiss = [0., 0., 0., 0., 0., 0.] #

def getJS(name = ''):
    global buttons
    #Retrieve any events
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION: #Analog sticks
            axiss[event.axis] = round(event.value, 2) #Store them in the list
        elif event.type == pygame.JOYBUTTONDOWN: #Button pressed
            #print(event.dict, event.joy, event.button, 'PRESSED')
            for x,(key,val) in enumerate(buttons.items()):
                if x < 10:
                    if controller.get_button(x):
                        buttons[key] = 1 #When button pressed, it changes the value to 1
        elif event.type == pygame.JOYBUTTONUP:
            #print(event.dict, event.joy, event.button, 'RELEASED')
            for x,(key,val) in enumerate(buttons.items()):
                if x < 10:
                    if event.button == x:
                        buttons[key] = 0 #When button is released it changes the value to 0

    #To remove element 2 since axis numbers are 0 1 3 4
    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] = [axiss[0], axiss[1], axiss[3], axiss[4]]

    if name == '':
        return buttons #Return all the bottoms
    else:
        return buttons[name] #Return the particular key we asked for

def main():
    #print(getJS()) #Get all values
    #sleep(0.05)
    print(getJS('share')) #Get only share button values
    sleep(0.05)

if __name__ == '__main__':
    while True:
        main()
