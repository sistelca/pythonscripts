#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def grafico(ax, x, x_lab, y, color, servidor, titulo=''):
    ax.plot(x, y, color = color)
    plt.xticks(x, x_lab, rotation = 50)
    for xx in x_lab:
        if len(xx) > 2:
            ejex = x[x_lab.index(xx)]
            ax.plot([ejex, ejex], [0,ax.axis()[3]], 'k-')
    ax.set(xlabel = 'hora', ylabel = 'cantidad',
           title = titulo)
    ax.text(3, 8, servidor, bbox = {'facecolor':color, 'alpha':0.5, 'pad':10})
    ax.grid()


def etiqs(lis):
    ejex = range(len(lis.Hora))
    ejex_lab = []

    for i in ejex:
        if i % 5 != 0: # remplazar esta condicion x cambio de fecha y horas criticas
            ejex_lab.append('')
        else:
            lab_c = lis.Fecha[ejex.index(i)]
            fin_c = lab_c.rindex('/')
            lab_c = lab_c[:fin_c]
            ejex_lab.append(lab_c+'\n'+lis.Hora[ejex.index(i)])

    return [ejex, ejex_lab]

url = 'http://192.168.35.75/activos.txt'

conecta75 = pd.read_csv(url, delimiter='\t')

conecta69 = pd.read_csv('/phoneadmin/conecta11.txt', delimiter='\t')

x1, x1_lab = etiqs(conecta75)
x2, x2_lab = etiqs(conecta69)

y1 = conecta75.Usuarios_conectados
y2 = conecta69.Usuarios_conectados

plt.figure(1)

ax1 = plt.subplot(211)
grafico(ax1, x1, x1_lab, y1, 'b', 'Adm Mercado', 'Usuarios conectados')

ax2 = plt.subplot(212)
grafico(ax2, x2, x2_lab, y2, 'g', 'Sec Casa')
plt.show()
