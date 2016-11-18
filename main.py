#!/usr/bin/env python
try:
	from funciones import*
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
	# por mientras, la weaita es que puedas ajustar el de cada pieza mientras tocas, osea cambiar la weaita en la lista del diccionario
	umbral = int(raw_input("Ingrese el umbral: ")) # el umbreal es la señal minima que envia el arduino
	for key,sound in zip(keys, sounds):#Junta la lista kit y keys para hacer una lista de tuplas que atribuye un sonido a una pieza, si la lista difieren de rango crea un diccionario con el rango menor de las listas
		key_sound[key]=list()
		key_sound[key].append(sound)
		key_sound[key].append(0)
		key_sound[key].append(umbral)# por mientras es la misma para todas
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
					pieza, intensidad = line.strip().split(",")
					if int(intensidad) >= umbral:
						if pieza in keys:
							lines.add(pieza)
							key_sound[pieza][1]+=1
							if key_sound[pieza][1] > 7:
								break
			for key in key_sound:
				key_sound[key][1]=0
		except:
			pass

		if len(lines) > 0:
			print lines
			for line in lines:
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
