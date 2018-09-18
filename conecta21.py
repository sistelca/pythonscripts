#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Conexion:

    def __init__(self, urlorigen):
        self.__urlorigen = urlorigen
        self.__conexdat = pd.read_csv(self.__urlorigen, delimiter='\t')
        self.x, self.x_lab = self.__etiqs(self.__conexdat)
        self.y = self.__conexdat.Usuarios_conectados

    def __etiqs(self, __conexdat):
        ejex = range(len(self.__conexdat.Hora))
        ejex_lab = []

        for i in ejex:
            if i % 10 != 0: # remplazar esta condicion x cambio de fecha y horas criticas
                ejex_lab.append('')
            else:
                lab_c = self.__conexdat.Fecha[ejex.index(i)]
                fin_c = lab_c.rindex('/')
                lab_c = lab_c[:fin_c]
                ejex_lab.append(lab_c+'\n'+self.__conexdat.Hora[ejex.index(i)])
        return ejex, ejex_lab

def grafico(ax, x, x_lab, y, color, servidor, titulo=''):
    # ax: objeto grafico
    # x: indice de eje x (lista de valores numericos)
    # x_lab: etiquetas para valores del eje x
    # y: valores del eje y (viene de el dataframe
    # color: color delcontexto grafico
    # servidor: identificacion del ordenador que envia los datos
    # titulo: titulo de grafico
    
    ax.plot(x, y, color = color)
    plt.xticks(x, x_lab, rotation = 50)
    for xx in x_lab:
        if len(xx) > 2:
            ejex = x[x_lab.index(xx)]
            ax.plot([ejex, ejex], [0,ax.axis()[3]], 'k-')
    ax.set(xlabel = 'hora', ylabel = 'cantidad',
           title = titulo)
    ax.text(3, 8, servidor, bbox = {'facecolor':color, 'alpha':0.3, 'pad':10})
    ax.grid()

plt.figure(1)

ax1 = plt.subplot(211)
casa = Conexion('http://192.168.35.75/activos.txt')
x1, x1_lab, y1 = casa.x, casa.x_lab, casa.y
grafico(ax1, x1, x1_lab, y1, 'b', 'Sec Casa', 'Usuarios conectados')

ax2 = plt.subplot(212)
merc = Conexion('http://192.168.35.69/activos.txt')
x2, x2_lab, y2 = merc.x, merc.x_lab, merc.y
grafico(ax2, x2, x2_lab, y2, 'g', 'Adm Mercado')
plt.show()
