#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
ax1.plot(x1, y1)
plt.xticks(x1, x1_lab, rotation=50)
for xx in x1_lab:
    if len(xx)>2:
        ejex = x1[x1_lab.index(xx)]
        ax1.plot([ejex, ejex], [0, ax1.axis()[3]], 'k-')
        
ax1.set(xlabel='hora', ylabel='cantidad',
       title='Usuarios conectados')
ax1.text(3, 8, '75', bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})
ax1.grid()


ax2 = plt.subplot(212)
ax2.plot(x2, y2, color = 'g')
plt.xticks(x2, x2_lab, rotation=50)
for xx in x2_lab:
    if len(xx)>2:
        ejex = x2[x2_lab.index(xx)]
        ax2.plot([ejex, ejex], [0, ax2.axis()[3]], 'k-')

ax2.set(xlabel='hora', ylabel='cantidad')
ax2.text(3, 8, '69', bbox={'facecolor':'green', 'alpha':0.5, 'pad':10})
ax2.grid()
plt.show()
