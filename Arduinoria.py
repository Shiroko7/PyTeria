#!/usr/bin/env python

from scipy.io import wavfile
import serial
import time
import pygame

arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=0.005)

def main():
    fps, hihat = wavfile.read("hihat.wav") # wavfile.read entrega una tupla con el frame y un array del archivo
    kick = wavfile.read("kick.wav")[1] #Este kit de bateria tienen todos el mismo fps
    crash = wavfile.read("openhat.wav")[1]
    ride = wavfile.read("ride.wav")[1]
    snare = wavfile.read("snare.wav")[1]
    tom1 = wavfile.read("tom1.wav")[1]
    tom2 = wavfile.read("tom2.wav")[1]

    kit = [snare, hihat, crash, tom1, tom2, ride, kick, kick] #kick,kick doble pedalTM

    sys.stdout.write('Transponding sound file... ')#Teclado pc
    sys.stdout.flush()


    pygame.mixer.init(fps, -16, 1, 2048)#Inicia el mixer

    screen = pygame.display.set_mode((350, 350))# Pequeña pantalla
    keys = ["1TOCANDO", "2TOCANDO"] #Nombre clave de una pieza de la bateria
    sounds = map(pygame.sndarray.make_sound, kit)
    key_sound = dict(zip(keys, sounds))#Junta la lista kit y keys para hacer un diccionario que atribuye un sonido a una pieza, si la lista difieren de rango crea un diccionario con el rango menor de las listas
    is_playing = {k: False for k in keys}# Diccionario que verifica si una pieza esta siendo tocada

    while True:
        event = pygame.event.wait()#Teclado pc
        line = arduino.readline()#Arduino

        if line != "":
            key = line.split(" ")[1]

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):#Si se toca una tecla en el pc
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN or line != "":
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:#Cierra el programa con ESC
                pygame.quit()
                raise KeyboardInterrupt

        elif (event.type == pygame.KEYUP or line == "") key and key in key_sound.keys():  #ni idea si esto funcione on el arduino, con el teclado responde cuando presionas una tecla y cuando la sueltas
            # Efecto fade out 50ms
            key_sound[key].fadeout(50)
            is_playing[key] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')