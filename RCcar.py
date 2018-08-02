from time import sleep, time
import RPi.GPIO as gp
from gpiozero import Buzzer, DistanceSensor
from itertools import chain
import curses


hold_time = 0.08   # 0.1 nebo 0.2 jsou vyzkoušené a fungují

safety_dist = 10   # vzdálenost, při které se spustí signalizace srážky

motor = [11, 12, 13, 15]
ultrasonic = {"front": {"pin": [35, 37], "GPIO":[19, 26]}, 
			  "back": {"pin": [38, 40], "GPIO":[20, 21]}}

red = 33; green = 32; blue = 31
Rgb = {"pins": [red, green, blue], "status": 0 }
buzz = {"pin": 36, "GPIO": 16, "On/Off":0}
global buzzer
global time_prev


process = True



def setup():
	gp.setmode(gp.BOARD)
	for pin in chain(motor, Rgb["pins"]):
		gp.setup(pin, gp.OUT)

	#inicializace bzučáku
	buzzer = Buzzer(buzz["GPIO"])

	#inicializace distance senzoru
	for pos in list(ultrasonic):
		gp.setup(ultrasonic[pos]["pin"][1], gp.OUT)
		gp.setup(ultrasonic[pos]["pin"][0], gp.IN)



def RGB(color):
	if color not in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
		raise ValueError("Tuto barvu neumím vytvořit")

	rgb = [1 - color[0], 1 - color[1], 1 - color[2]]
	for i,j in enumerate(Rgb["pins"]):
		gp.output(j, rgb[i])
	Rgb["status"] = not Rgb["status"] 



def red_blink():
	if Rgb["status"]:
		RGB([1,0,0])
		print("light on")
	else: 
		RGB([0,0,0])
		print("light off")

def forward():
	#setup()
	#Turn ON
	RGB([0,0,1])
	gp.output(motor[0], True)
	gp.output(motor[1], False)
	gp.output(motor[2], False)
	gp.output(motor[3], True)
	sleep(hold_time)
	#Turn OFF
	gp.output(motor[0], False)
	gp.output(motor[3], False)
	RGB([0,0,0])
	#gp.cleanup()

def backward():
    #Turn ON
    RGB([0,1,0])
    gp.output(motor[0], False)
    gp.output(motor[1], True)
    gp.output(motor[2], True)
    gp.output(motor[3], False)
    sleep(hold_time)
    #Turn OFF
    gp.output(motor[1], False)
    gp.output(motor[2], False)
    RGB([0,0,0])

def right():
    #Turn ON
    gp.output(motor[0], True)
    gp.output(motor[1], False)
    gp.output(motor[2], True)
    gp.output(motor[3], False)
    sleep(hold_time)
    #Turn OFF
    gp.output(motor[0], False)
    gp.output(motor[2], False)

def left():
    #Turn ON
    gp.output(motor[0], False)
    gp.output(motor[1], True)
    gp.output(motor[2], False)
    gp.output(motor[3], True)
    sleep(hold_time)
    #Turn OFF
    gp.output(motor[1], False)
    gp.output(motor[3], False)

def measure_distance(position):
	if position not in list(ultrasonic):
		raise ValueError("Není žádný senzor na zadané pozici")
	else:
		gp.output(ultrasonic[position]["pin"][1], True)
		sleep(0.0001)
		gp.output(ultrasonic[position]["pin"][1], False)

		while gp.input(ultrasonic[position]["pin"][0]) == False:
			start = time()

		while gp.input(ultrasonic[position]["pin"][0]) == True:
			end = time()

		signal_time = end-start
		return signal_time / 0.000058 #cm

def Check_distance():
	
	distance = int(min(measure_distance("front"),measure_distance("back"))) 
	
	if distance < safety_dist
		Colizion()
	elif distance > safety_dist and buzz["On/Off"] = 1:
		buzzer.off()
		buzz["On/Off"] = 0
	else:
		pass

def Colizion():
	time_now = int(time()) 
	if time_prev < time_now:
		if buzz["On/Off"] == 0; 
			buzzer.on()
			buzz["On/Off"] = 1
			RGB([1,0,0])
		else:
			buzzer.off()
			buzz["On/Off"] = 0
			RGB([0,0,0])
	


#Main body


screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
try:
	time_prev = int(time())
	while process:
		Check_distance()
		char = screen.getch()
		if char == ord('q'):
			process = False
			break
		elif char == ord('w'):
			forward()
		elif char == ord('s'):
			backward()
		elif char == ord('a'):
			left()
		elif char == ord('d'):
			right()
		elif char == curses.KEY_UP:
			forward()
		elif char == curses.KEY_DOWN:
			backward()
		elif char == curses.KEY_LEFT:
			left()
		elif char == curses.KEY_RIGHT:
			right()
		elif char == ord('b'):
			red_blink()
		else:
			pass



finally:
	process = False
	curses.nocbreak()
	screen.keypad(False)
	curses.echo()
	curses.endwin()
	gp.cleanup()


