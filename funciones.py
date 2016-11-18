from scipy.io import wavfile
import serial
import pygame
import sys
import os
from pygame.locals import *

def searchsound(path): # Busca todos los sonidos ha tocar dada un directorio
	sounds = list()
	for folder in os.listdir("kits"):
		if folder == path:
			for sound in os.listdir("kits/" + folder):
				name, ext = os.path.splitext(sound)
				if ext == ".wav":
					fps,file = wavfile.read(os.path.join("kits", folder, sound))
					sounds.append(file)
	return (fps,sounds)

def searchconf(): # Busca la configuracoines guardadas anteriormente
	configs = list()
	for cfg in os.listdir("configs"):
		name, ext = os.path.splitext(cfg)
		if ext == ".cfg":
			configs.append(name)
	return configs

def pickconf(archivo): # accede a la configuracion con el nombre del archivo
	for cfg in os.listdir("configs"):
		name, ext = os.path.splitext(cfg)
		if name == archivo:
			with open(os.path.join(("configs"), cfg), "r") as config:
				line = config.readline()
				path, piezas = line.split(";;")
	return (path, piezas)

def writeconf(name): # Escribe una configuracion nueva
	with open(os.path.join(("configs"), name), "w") as newconf:
		folder = raw_input("Ingrese el nombre del pack de sonidos: ")
		number = int(raw_input("Ingrese el numero de piezas de la bateria: "))
		piezas = ""
		for i in range(number):
			pieza = raw_input("Ingrese el nombre de la pieza "+str(i+1)+" : ")
			piezas.join(pieza+"::")
		ccc="".join(folder+";;").join(number+";;").join(piezas)
		newconf.write(ccc)


def conf(): # Funcion tipo main que deberia estar hecha como interfaz grafica
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
			try:
				config = raw_input("Input: ")
				cfg = pickconf(config)
				print "Confirma3: ", config
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
