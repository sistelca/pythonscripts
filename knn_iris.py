# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 15:22:28 2018

@author: Luis
"""

# practica clase nº 7. datos iris

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mglearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

def indices_general(MC, nombres = None):
    precision_global = np.sum(MC.diagonal()) / np.sum(MC)
    error_global = 1 - precision_global
    presicion_categoria = pd.DataFrame(MC.diagonal()/np.sum(MC, axis = 1)).T
    if nombres!=None:
        presicion_categoria.columns = nombres
    return {"Matriz de Confucion": MC,
            "Precision Global": precision_global,
            "Error Global": error_global,
            "Precision por categoria":presicion_categoria}
    
os.chdir("/Users/Luis/Documents")
iris = pd.read_csv('iris.csv', delimiter=',',decimal='.',index_col=None)

# verificar si los datos fueron bien cargados

print(iris.head())
print(iris.shape)
iris.info()

X = iris.iloc[:,:4]
y = iris.iloc[:,4]

print(X.head())
print(y.head())

# 70% de los datos para entrenamiento

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=0)

# mediante el constructor inicializa el atributo 
# n_neighbors=3

instancia_knn = KNeighborsClassifier(n_neighbors=3)

instancia_knn.fit(X_train, y_train)

print("Las predicciones en Testing son: {}".format(instancia_knn.predict(X_test)))

# Porcentaje de prediccion global

print("Prediccion en Testing: {:.2f}".format(instancia_knn.score(X_test, y_test)))

# Matriz de confusion

prediccion = instancia_knn.predict(X_test)
MC = confusion_matrix(y_test, prediccion)
print("Matriz de Confusion: \n{}".format(MC))

# indices de calidad del modelo

indices = indices_general(MC)

for k in indices:
    print("\n%s:\n%s"%(k,str(indices[k])))














