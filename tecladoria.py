#!/usr/bin/env python

from scipy.io import wavfile
import numpy as np
import pygame
import sys

"""def speedx(snd_array, factor):
	# Speeds up / slows down a sound, by some factor.
		indices = np.round(np.arange(0, len(snd_array), factor))
		indices = indices[indices < len(snd_array)].astype(int)
		return snd_array[indices] """


"""def stretch(snd_array, factor, window_size, h):
    # Stretches/shortens a sound, by some factor. 
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(len(snd_array) / factor + window_size)

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')"""


def main():
    fps, hihat = wavfile.read("hihat.wav")
    kick = wavfile.read("kick.wav")[1]
    crash = wavfile.read("openhat.wav")[1]
    ride = wavfile.read("ride.wav")[1]
    snare = wavfile.read("snare.wav")[1]
    tom1 = wavfile.read("tom1.wav")[1]
    tom2 = wavfile.read("tom2.wav")[1]

    kit = [snare, hihat, crash, tom1, tom2, ride, kick, kick]

    sys.stdout.write('Transponding sound file... ')
    sys.stdout.flush()
    print('DONE')

    # MIXER
    pygame.mixer.init(fps, -16, 1, 2048)
    #SCREEN
    screen = pygame.display.set_mode((350, 350))
    keys = ["c", "d", "r", "g", "h", "k", "n", "m"]
    sounds = map(pygame.sndarray.make_sound, kit)
    key_sound = dict(zip(keys, sounds))
    is_playing = {k: False for k in keys}

    while True:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            is_playing[key] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
