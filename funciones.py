from scipy.io import wavfile
import serial
import pygame
import sys
import os
from easygui import*
from pygame.locals import *

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


def searchsound(path): #Busca los sonidos en un directorio
	sounds = list()
	for sound in os.listdir(path):
		name, ext = os.path.splitext(sound)
		if ext == ".wav":
			sounds.append(name)
	return sounds

def picksound(path,nombre): #Devuelve el puntero de un sonido wav
	for sound in os.listdir("kits/"+path):
		name, ext = os.path.splitext(sound)
		if nombre == name and ext == ".wav":
			fps,file = wavfile.read(os.path.join("kits", path, sound))
			return file


def pickfps(path): # Busca la frecuencia
	for sound in os.listdir("kits/" + path):
		name, ext = os.path.splitext(sound)
		if ext == ".wav":
			fps,file = wavfile.read(os.path.join("kits", path, sound))
	return fps

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

def writeconf(name,titulo): # Escribe una configuracion nueva
	with open(os.path.join(("configs"), name + ".cfg"), "w") as newconf:
		msgbox("Ingrese el nombre del pack de sonidos")
		folder= diropenbox(titulo)
		piezas = set()
		botones = searchsound(folder)
		numero = enterbox("Ingrese el numero de pads disponible")
		ccc = ""
		ccc = folder.split("/")[-1]+";;"
		espectros = open(os.path.join(("configs"),"piezas.txt"),"r")
		espectro = espectros.readline()
		espec = espectro.split("::")
		variable = 0
		while True:
			lines = set()
			choice = buttonbox("Escoja un sonido", titulo, botones)
			valor = 0
			a = ""
			try:
				while a != "Break":
					try:
						line = arduino.readline()
						while line != "":
							line = arduino.readline()
							pieza, intensidad = line.strip().split(",")
							if pieza in espec:
								lines.add(pieza)
						if len(lines) > 0:
							a = "Break"
					except:
						pass
				for lectura in lines:
					pieza = lectura
				for i in piezas:
					try:
						if i.split(".")[0] == pieza:
							valor = 1
					except:
						pass
				if valor == 0:
					piezas.add(pieza + "." + choice)
					msgbox("Se le asigno " + choice + " a " + pieza)
					del botones[botones.index(choice)]
					variable +=1
				if variable == int(numero):
					break
				if valor == 1:
					msgbox("Seleccione una pieza distinta")
			except:
				pass
		xd = 0
		for pieza in piezas:
			if xd != 0:
				ccc = ccc+"::"+pieza
			else:
				ccc = ccc+pieza
			xd+=1
		newconf.write(ccc)
		newconf.close()
		espectros.close()

def delconf(archivo): #Borra una configuracion
	for cfg in os.listdir("configs"):
		name, ext = os.path.splitext(cfg)
		if ext == ".cfg":
			if name == archivo:
				os.remove(os.path.join(("configs"),name+".cfg"))

def main(cfg):
	folder = cfg[0]
	keys = cfg[1].split("::")
	fps = pickfps(folder)
	key_sound =dict()
	umbral = 10 #potencia minima de lectura
	pygame.mixer.init(fps, -16, 1, 2048)#Inicia el mixer
	for key in keys:
		array = picksound(folder, key.split(".")[1])
		key_sound[key.split(".")[0]] = list()
		key_sound[key.split(".")[0]].append(pygame.sndarray.make_sound(array)) #transforma el puntero en uno que lea el sonido
		key_sound[key.split(".")[0]].append(0) #Evite multilecturas
	lines = set()
	i = 0
	opcion = ""
	while opcion != "Break":
		try:
			line = arduino.readline()
			while line != "":
				line = arduino.readline()
				enil = line.strip().split(",")
				if int(enil[1]) >= umbral:
					if enil[0] in key_sound:
						lines.add(enil[0])
						key_sound[enil[0]][1]+=1
						if key_sound[enil[0]][1] > 7:
							break
			for key in key_sound:
				key_sound[key][1]=0
		except:
			pass

		if len(lines) > 0:
			for line in lines:
				key_sound[line][0].play()
			lines = set()
