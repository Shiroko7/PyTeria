#!/usr/bin/env python
try:
	from scipy.io import wavfile
	import serial
	import pygame
	import sys
	import os
	from pygame.locals import *
except:
	print "Para el funcionamiento de este programa se necesitan las siguientes librerias: serial, pygame y scipy"

try:
	arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=0.005)
except:
	pass

try:
	arduino = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=0.005)
except:
	pass

try: 
	arduino = serial.Serial('/dev/ttyACM2', baudrate=9600, timeout=0.005)
except:
	pass

def searchsound(path):
	sounds = list()
	for folder in os.listdir("kits"):
		if folder == path:
			for sound in os.listdir("kits/" + folder):
				name, ext = os.path.splitext(sound)
				if ext == ".wav":
					fps,file = wavfile.read(os.path.join("kits", folder, sound))
					sounds.append(file)
	return (fps,sounds)

def searchconf():
	configs = list()
	for cfg in os.listdir("configs"):
		name, ext = os.path.splitext(cfg)
		if ext == ".cfg":
			configs.append(name)
	return configs

def pickconf(archivo):
	for cfg in os.listdir("configs"):
		name, ext = os.path.splitext(cfg)
		if name == archivo:
			with open(os.path.join(("configs"), cfg), "r") as config:
				line = config.readline()
				path, piezas = line.split(";;")
	return (path, piezas)

def writeconf(name):
	with open(os.path.join(("configs"), name), "w") as newconf:
		folder = raw_input("Ingrese el nombre del pack de sonidos: ")
		number = int(raw_input("Ingrese el numero de piezas de la bateria: "))
		piezas = ""
		for i in range(number):
			pieza = raw_input("Ingrese el nombre de la pieza "+str(i+1)+" : ")
			piezas.join(pieza+"::")
		ccc="".join(folder+";;").join(number+";;").join(piezas)
		newconf.write(ccc)


def conf():
	a=""
	while a != "3":
		print "1 Elegir configuracion\n2 Crear configuracion\n3 Salir"
		a = raw_input("Opcion: ")
		if a == "1":
			config = searchconf()
			e = 1
			for conf in config:
				print e, conf
				e+=1
			print "Escriba el nombre de la configuracion"
			for i in configuraciones:
				e+=1
				print str(e) + " " + i
			try:
				config = raw_input("Input: ")
				cfg = pickconf(config)
			except:
				print "Introdusca una configuracion valida"
		elif a == "2": #WORK IN PROGRESS
			print "Escriba el nombre de la nueva configuracion"
			b = raw_input("Nombre: ")
			try:
				writeconf(b)
			except:
				print "Error en la configuracion, Intente nuevamente"
	return cfg

def main(cfg):
	screen = pygame.display.set_mode((350, 350))# GUI
	sys.stdout.write("INICIALIZANDO...\n")#Teclado pc
	sys.stdout.flush()

	folder = cfg[0]
	keys = cfg[1].split("::")
	fps, kit = searchsound(folder)
	pygame.mixer.init(fps, -16, 1, 2048)#Inicia el mixer
	sounds = map(pygame.sndarray.make_sound, kit)
	key_sound = dict()
	for key,sound in zip(keys, sounds):#Junta la lista kit y keys para hacer una lista de tuplas que atribuye un sonido a una pieza, si la lista difieren de rango crea un diccionario con el rango menor de las listas
		key_sound[key]=list()
		key_sound[key].append(sound)
		key_sound[key].append(0)
	key = "xd"
	F = ""
	lines = set()
	i = 0
	while F != "break":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise KeyboardInterrupt
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					raise KeyboardInterrupt
				if event.key == pygame.K_SPACE:
					F = "break"
		try:
			line = arduino.readline()
			if line != key:
				while line != "":
					line = arduino.readline()
					key = line.strip()
					if key in keys:
						lines.add(key)
					"""i+=1
					print i
					if i > 12:
						break
			i=0"""
		except:
			pass

		if len(lines) > 0:
			print lines
			for line in lines:
				if key_sound[line][1] == 0:
					key_sound[line][0].play()
			lines = set()



if __name__ == '__main__':
	try:
		a = ""
		cfg = pickconf("Basic")
		while a != "3":
			print "INTERFAZ DE PRUEBA\n1 Iniciar\n2 Configurar\n3 Salir"
			a = raw_input("Opcion: ")
			if a == "2":
				cfg = conf()
			elif a == "1":
				main(cfg)
			else:
				print "Seleccione una opcion valida"
	except KeyboardInterrupt:
		print "\nOVER\n"
