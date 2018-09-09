#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import json

def leadispo( num = 0):
    if num == 0:
        comando = ['gnokii --showsmsfolderstatus']
    else:
#        comando = 'gnokii --getsms SM 0 '+str(num - 1)+' -d'
        comando = ['/usr/bin/gnokii --getsms SM 0 ' + str(num - 1)]

    conte = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    return conte

def leamensje(linea, i):
    if linea.count('Inbox Message') > 0:
        valor = i
    elif linea.count('Date/time') > 0:
        valor = linea[linea.find(':')+2:-7]
    elif linea.count('Sender') > 0:
        valor = linea[linea.find(':')+2:linea.find('Msg')-1]
    elif linea.count('Text') > 0 or linea.count('Linked') > 0:
        valor = None
    elif linea.count('GNOKII') > 0:
        valor = None
    else:
        valor = linea
        
    return valor

def myFunc(e):
  return (e['Enviado/por'])
    

# leyendo tabla resumen de mensajes
contenido = leadispo(0)

while True:
    linea = contenido.stdout.readline()
    if linea.count('SM') > 0:
        numesg = int(linea[-3:])
        break

# leyendo todos los mensajes
mensajes = leadispo(numesg)
jns_mensajes = []
claves = ["ID", "Fecha/Hora", "Enviado/por", "Texto"]
valores = []
# usar zip para agregar en append el otro diccionario
i = 0
while True:
    linea = mensajes.stdout.readline()
    conte = leamensje(linea, i)

    print(conte!=None, '---', conte)

    if conte != None and conte!='\n':
        valores.append(conte)

    if conte == linea and conte!='\n':
        if len(claves) == len(valores):
            jns_mensajes.append(dict(zip(claves[1:], valores[1:])))
            i += 1

        valores= []
        
    if linea == '':
        break
form = json.dumps(jns_mensajes, indent = 4, sort_keys=False)

print(form)

print(len(jns_mensajes))
jns_mensajes.sort(key=myFunc)
with open('/var/www/html/mensajes.json', 'a') as archivo:
    archivo.write(json.dumps(jns_mensajes, indent= 4, sort_keys=False))

