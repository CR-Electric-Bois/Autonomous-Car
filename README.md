# Autonomous car
This projects consist in making an autonomous car using an RC one and a Raspberry Pi to control it. We are also using a Camera Module so that the car can drive by itself.

## Robot-main
This Python code works to call the module files to control the car.

## Motor-Module
Python code to control both motors in the car
The motor in the front of the car controls the direction only, the pins of the GPIO of the Raspberry Pi to control it are: 20, 16, and 12.
The motor in the back fo the car is for the speed only, the pins of the GPIO of the Raspberry Pi to control it are: 25, 24 and 23.

## Joystick-Module
Python code to obtain the values of a PS4 controller. In this code we use values of 1 0r 0 for the buttons in the controller to know when they are pressed or not. Also we use the axis of the Joystick and give values from -1 to 1 to know the position. The idea of the controller is for test drives of the car to collect information.
