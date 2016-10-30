#!/usr/bin/env python
try:
	from scipy.io import wavfile
	import serial
	import pygame
	import sys
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

def readconf(archivo = "kit1.txt"):
	ss = open(archivo)
	asdf = ss.readline()
	ss.close()
	return asdf.split(";;")

def conf():
	a=""
	while a != "3":
		print "1 Elegir configuracion\n2 Crear configuracion\n3 Salir"
		a = raw_input("Opcion: ")
		if a == "1":
			config = open("conf.txt", "r")
			configuraciones = config.split("::")
			e = 0
			print "Escriba el nombre de la configuracion"
			for i in configuraciones:
				e+=1
				print str(e) + " " + i
			try:
				cfg = raw_input("Input: ")
			except:
				print "Introdusca una configuracion valida"
			config.close()
		elif a == "2": #WORK IN PROGRESS
			print "Escriba el nombre de la nueva configuracion"
			b = raw_input("Nombre: ")
			config = open("conf.txt", "a")
			newcfg = open( b + ".txt", "w")
			config.write("::"+b)
			config.close()

def main():
	try:
		cfgs = readconf(cfg)
	except:
		cfgs = readconf()

	#folder = cfgs[0]         #Por aplicar
	#kit = cfgs[1].split("::")
	keys = cfgs[2].split("::")   #Nombre clave de una pieza de la bateria
	fps, hihat = wavfile.read("hihat.wav") # wavfile.read entrega una tupla con el frame y un array del archivo
	kick = wavfile.read("kick.wav")[1] #Este kit de bateria tienen todos el mismo fps
	crash = wavfile.read("openhat.wav")[1]
	ride = wavfile.read("ride.wav")[1]
	snare = wavfile.read("snare.wav")[1]
	tom1 = wavfile.read("tom1.wav")[1]
	tom2 = wavfile.read("tom2.wav")[1]

	kit = [snare, hihat, crash, tom1, tom2, ride, kick]

	sys.stdout.write("VERSiON DE PRUEBA")#Teclado pc
	sys.stdout.flush()


	pygame.mixer.init(fps, -16, 1, 2048)#Inicia el mixer

	screen = pygame.display.set_mode((350, 350))# GUI

	sounds = map(pygame.sndarray.make_sound, kit)
	key_sound = dict(zip(keys, sounds))#Junta la lista kit y keys para hacer un diccionario que atribuye un sonido a una pieza, si la lista difieren de rango crea un diccionario con el rango menor de las listas
	key = ""
	Partes = [0 for i in keys]  #Evita repeticion, multilecturas
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise KeyboardInterrupt
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					raise KeyboardInterrupt
		line = arduino.readline()#Arduino
		if line != "":
			key = line.strip()
			if key == "TOCANDO1":
				Partes[0]+=1
			if key == "TOCANDO2":
				Partes[1]+=1
			if key == "TOCANDO3":
				Partes[2]+=1
			if key == "TOCANDO4":
				Partes[3]+=1
			if key == "TOCANDO5":
				Partes[4]+=1
			if key == "TOCANDO6":
				Partes[5]+=1
			if key == "TOCANDO7":
				Partes[6]+=1

			e=0
			for i in Partes:
				if i > 11:
					key_sound[key].play()
					Partes[e] = 0
				e+=1

if __name__ == '__main__':
	try:
		a = ""
		while a != "3":
			print "INTERFAZ DE PRUEBA\n1 Iniciar\n2 Configurar\n3 Salir"
			a = raw_input("Opcion: ")
			if a == "2":
				conf()
			elif a == "1":
				main()
			else:
				print "Seleccione una opcion valida"
	except KeyboardInterrupt:
		print "\nOVER\n"
