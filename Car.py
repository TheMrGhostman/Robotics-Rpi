import RPi.GPIO as gpio
from time import sleep, time
from gpiozero import Buzzer, DistanceSensor
from itertools import chain

class robocar:
	"""
	- gpio.setmode(gpio.BOARD) jsem zadefinoval natvrdo znovu // ještě je třeba prověřit
	- knihovna je určena k snadnějšímu ovládání motorů s H-Bridgem L298N
		a předpřipravena pro nastavení rychosti pomocí PWM (zatím není otestováno)

	"""

	def __init__(self, motor_pins, hold_time, pwm_pins=[], speed=100, freq=100):
		if speed > 100 or speed < 0:
			raise ValueError("Zadaná rychlost je příliš vysoká nebo záporná!!")
		if not isinstance(motor_pins, list) or len(motor_pins) < 4:
			raise ValueError("Piny motoru jsou zadané špatně!!")
		self.motor_pins = motor_pins
		self.hold_time = hold_time
		self.speed = speed
		self.pwm_pins = pwm_pins
		self.pwm = []
		self.freq = freq
		self.set_pwm()

	def setup(self):
		gpio.setmode(gpio.BOARD)
		for pin in chain(self.motor_pins, self.pwm_pins):
			gpio.setup(pin, gpio.OUT)
		self.stop()

	def set_pwm(self): 
		for i,j in enumerate(self.pwm_pins):
			self.pwm.append(gpio.PWM(j, self.freq))
			self.pwm[i].start(self.speed)

	def stop(self):
		for pin in self.motor_pins:
			gpio.output(pin, False)

	def change_speed(self, new_speed):
		self.speed = new_speed

	def change_hold_time(self, new_hold_time):
		self.hold_time = new_hold_time

	def set_speed():
		if self.speed != 100:
			for p in self.pwm:
				p.ChangeDutyCycle(self.speed)
		else:
			pass

	def forward(self):
		self.set_speed()
		gpio.output(self.motor_pins[0], True)
		gpio.output(self.motor_pins[1], False)
		gpio.output(self.motor_pins[2], False)
		gpio.output(self.motor_pins[3], True)
		sleep(self.hold_time)
		self.stop()

	def backward(self):
		self.set_speed()
		gpio.output(self.motor_pins[0], False)
		gpio.output(self.motor_pins[1], True)
		gpio.output(self.motor_pins[2], True)
		gpio.output(self.motor_pins[3], False)
		sleep(self.hold_time)
		self.stop()

	def right(self):
		self.set_speed()
		gpio.output(self.motor_pins[0], True)
		gpio.output(self.motor_pins[1], False)
		gpio.output(self.motor_pins[2], True)
		gpio.output(self.motor_pins[3], False)
		sleep(self.hold_time)
		self.stop()

	def left(self):
		self.set_speed()
		gpio.output(self.motor_pins[0], False)
		gpio.output(self.motor_pins[1], True)
		gpio.output(self.motor_pins[2], False)
		gpio.output(self.motor_pins[3], True)
		sleep(self.hold_time)
		self.stop()

	def hard_right(self):
		self.set_speed()
		gpio.output(self.motor_pins[0], True)
		sleep(self.hold_time)
		self.stop()

	def hard_left(self):
		self.set_speed()
		gpio.output(self.motor_pins[3], True)
		sleep(self.hold_time)
		self.stop()
