# coding: utf-8

import speech_recognition as sr
from pydub import AudioSegment
import os
import time
from threading import Thread


import pyaudio
import wave

activo = False


def nom_arch(dir):
    dirs = os.listdir( dir )
    dirs = [arch for arch in dirs if not os.path.isdir(arch) and 'chunk' in arch]
    return 'chunk' + str(len(dirs)+1).zfill(5) + '.wav'


def grabar():

    #DEFINIMOS PARAMETROS
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    CHUNK=1024
    duracion=10

    carpeta = './v2t'
    archivo = nom_arch(carpeta)

    #INICIAMOS "pyaudio"
    audio=pyaudio.PyAudio()

    #INICIAMOS GRABACIÓN
    stream=audio.open(format=FORMAT,channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    #print("grabando...")
    frames=[]

    for i in range(0, int(RATE/CHUNK*duracion)):
        data=stream.read(CHUNK)
        frames.append(data)
    #print("grabación terminada")

    #DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    waveFile = wave.open(carpeta + '/' + archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def voz2txt(file):
    # transcribe audio file                                                         
    AUDIO_FILE = file
                                 
    r = sr.Recognizer()

    try:
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file                  

            # recognize speech using Sphinx
            txt = ''
            try:
                txt = r.recognize_google(audio, language="es-ES")
                print(f"{file} dice: " + txt)
            except sr.UnknownValueError:
                print("Google could not understand audio")
            except sr.RequestError as e:
                print("Google error; {0}".format(e))
            except:
                pass
    except:
        txt = ''
    return txt


def convertir():

    path = "./v2t"

    dirs = os.listdir( path )
    dirs = sorted([arch for arch in dirs if not os.path.isdir(arch) and 'chunk' in arch])

    if len(dirs) > 0:

        for trozo in dirs:
            start_time = time.time()
            txt = voz2txt(path + '/' + trozo)

            with open('dialogo.txt', 'a+') as arch:
                if len(txt) > 0:
                    arch.write(txt + ' \n')
            #os.rename(path + '/' + trozo, path + '/_' + trozo[1:])
            try:
                os.remove(path + '/' + trozo)
            except:
                pass

            print(f'duration = {time.time() - start_time}')

def comenzar_grabar():
    global activo
    start_time = time.time()
    while True:
        grabar()
        if time.time() - start_time > 1500:
            activo = False
            break

def comenzar_convertir():
    global activo
    while True:
        convertir()
        if not activo:
            break

#########################################################################
#### Start the recording and start service to recognize the stream ######
#########################################################################

print("Enter CTRL+C to end recording...")

if __name__ == "__main__":

    try:
        grabar_thread = Thread(target=comenzar_grabar)
        activo = True
        recognize_thread = Thread(target=comenzar_convertir)
        with open('dialogo.txt', 'w') as arch:
            arch.write('')

        grabar_thread.start()
        recognize_thread.start()
    except:
        pass

    #    while True:
    #        pass 
    #except KeyboardInterrupt:
    #    # stop recording
    #    pass
