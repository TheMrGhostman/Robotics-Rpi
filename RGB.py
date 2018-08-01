import RPi.GPIO as gp
from time import sleep

red = 33
green = 32
blue = 31

def setting():
	gp.setmode(gp.BOARD)
	for i, j in enumerate([red, green, blue]):
		gp.setup(j, gp.OUT)

def b():
	gp.output(green, 1)
	gp.output(red, 1)
	sleep(2)
	gp.output(green, 0)
	gp.output(red,0)


def r():
	gp.output(green, 1)
	gp.output(blue, 1)
	sleep(2)
	gp.output(green, 0)
	gp.output(blue,0)

def g():
	gp.output(blue, 1)
	gp.output(red,1)
	sleep(2)
	gp.output(blue, 0)
	gp.output(red,0)

def clean():
	gp.cleanup()
