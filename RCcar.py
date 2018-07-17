from time import sleep
import RPi.GPIO as gp
import tkinter as tk

pins = [11, 12, 13, 15]
hold_time = 0.2

def setup():
	gp.setmode(gp.BOARD)

	for pin in pins:
		gp.setup(pin, gp.OUT)

def forward():
	setup()
	gp.output(pins[0], True)
	gp.output(pins[1], False)
	gp.output(pins[2], False)
	gp.output(pins[3], True)
	sleep(hold_time)
	gp.cleanup()

def backward():
        setup()
        gp.output(pins[0], False)
        gp.output(pins[1], True)
        gp.output(pins[2], True)
        gp.output(pins[3], False)
        sleep(hold_time)
        gp.cleanup()

def left():
        setup()
        gp.output(pins[0], True)
        gp.output(pins[1], False)
        gp.output(pins[2], True)
        gp.output(pins[3], False)
        sleep(hold_time)
        gp.cleanup()

def right():
        setup()
        gp.output(pins[0], False)
        gp.output(pins[1], True)
        gp.output(pins[2], False)
        gp.output(pins[3], True)
        sleep(hold_time)
        gp.cleanup()


def Key_Press(event):
	keypress = event.char
	if keypress.lower() == 'w':
		print("jedu dopředu")
		forward()
	elif keypress.lower() == 's':
		print("jedu dozadadu")
		backward()
	elif keypress.lower() == 'a':
		print("jedu vlevo")
		left()
	elif keypress.lower() == 'd':
		print("jedu vlevo")
		right()
	else:
		pass

command = tk.Tk()
command.bind('<KeyPress>', Key_Press)
command.mainloop()


