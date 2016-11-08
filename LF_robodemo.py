__author__ = 'keithd'

import random
from time import sleep

import image_manager as IMR
from sensors.camera import Camera
from sensors.motors import Motors
from sensors.reflectance_sensors import ReflectanceSensors
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.zumo_button import ZumoButton


## BE SURE TO RUN THESE DEMOS ON THE FLOOR or to have plenty of people guarding
## #  the edges of a table if it is run there.

# This just moves the robot around in a fixed dance pattern.  It uses no sensors.

def test():
    u = ReflectanceSensors()
    while True:
        u.update()
        v = u.get_value()
        sleep(2)
        print(v)

def dancer():
    ZumoButton().wait_for_press()
    m = Motors()
    m.forward(.2,3)
    m.backward(.2,3)
    m.right(.5,3)
    m.left(.5,3)
    m.backward(.3,2.5)
    m.set_value([.5,.1],10)
    m.set_value([-.5,-.1],10)

# This tests the UV (distance) sensors.  The robot moves forward to within 10 cm of the nearest obstacle.  It
# then does a little dancing before backing up to approximately 50 cm from the nearest obstacle.

def explorer(dist=10):
    ZumoButton().wait_for_press()
    m = Motors(); u = UltrasonicSensor()
    while u.update() > dist:
        m.forward(.2,0.2)
    m.backward(.1,.5)
    m.left(.5,3)
    m.right(.5,3.5)
    sleep(2)
    while u.update() < dist*5:
        m.backward(.2,0.2)
    m.left(.75,5)



def random_step(motors,speed=0.25,duration=1):
    dir = random.choice(['forward','backward','left','right'])
    eval('Motors.'+ dir)(motors,speed,duration)

# This moves around randomly until it gets to a dark spot on the floor (detected with the infrared belly sensors).
# It then rotates around, snapping pictures as it goes.  It then pastes all the pictures together into a
# panoramo view, many of which may be created per "vacation".

def tourist(steps=25,shots=5,speed=.25):
    ZumoButton().wait_for_press()
    rs = ReflectanceSensors(); m = Motors(); c = Camera()
    for i in range(steps):
        random_step(m,speed=speed,duration=0.5)
        vals = rs.update()
        if sum(vals) < 1:  # very dark area
            im = shoot_panorama(c,m,shots)
            im.dump_image('vacation_pic'+str(i)+'.jpeg')

def shoot_panorama(camera,motors,shots=5):
    s = 1
    im = IMR.ImageManager(image=camera.update()).scale(s, s)
    rotation_time = 3/shots # At a speed of 0.5(of max), it takes about 3 seconds to rotate 360 degrees
    for i in range(shots-1):
        motors.right(0.5,rotation_time)
        im = im.concat_horiz(IMR.ImageManager(image=camera.update()))
    return im

