'''
    Proyecto DATA SCIENCE - Fase 1
    Se solicita realizar de forma automatizada el Análisis Exploratorio de Datos de un dataframe dado en forma de archivo.csv
    
    Grupo 4:
        - Herber Sebastián Silva Muñoz
        - Eunice Anahí Mata Ixcayau
        - José Andrés Auyón Cóbar
        - Erick Stiv Junior Guerra Muñoz
'''

# Importación de librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
import sys

path = input("Ingrese el archivo csv a analizar: ")
X = readCSV(path)

if type(X) == str:
    print(X)
    sys.exit()
    
categorical, continuous, discreet = identifyVariables(X)

print("\nVariables categóricas:")
for i, col in enumerate(categorical, 1):
    print(f"{i}. {col}")

print("\nVariables numéricas contínuas:")
for i, col in enumerate(continuous, 1):
    print(f"{i}. {col}")

print("\nVariables numéricas discretas:")
for i, col in enumerate(discreet, 1):
    print(f"{i}. {col}")
    
null_values = getNulls(X)

if len(null_values) > 0:
    print("\nEl dataset cotiene valores nulos:")
    for t in null_values:
        print(f"La columna '{t[0]}' contiene {t[1]} valores nulos ({t[2]*100:.2f}% del total).")
    
numerics = continuous + discreet

statistics = getStatistics(X, numerics)

if len(statistics) > 0:
    print("\nA continuación, se listan las estadítsicas descriptivas para cada variable numérica:")

    for col, st in statistics.items():
        print(f"Variable {col}:")
        print(f"Media: {st[0]}")
        print(f"Mediana: {st[1]}")
        print(f"Moda: {st[2]}")
        print(f"Desviación Estándar: {st[3]}\n")
        
option = getOption("¿Desea generar gráficos?\n1. Sí\n2. No\n", 2)

if option == 2:
    print("¡Gracias por utilizar el programa!")
    sys.exit()

graphing = True

while(graphing):

    chosen = []
    choosing = True

    while choosing:
        variables = [col for col in list(X.columns) if col not in chosen]
        for i, col in enumerate(variables, 1):
            print(f"{i}. {col}")

        option = getOption("Seleccione una variable:",len(variables))

        var = variables[option-1]
        chosen.append(var)

        option = getOption("¿Seleccionar variable adicional?\n1. Sí\n2. No\n", 2)

        if option == 2:
            choosing = False
            
    graphingThis = True
    
    while graphingThis:
            
        if len(chosen) == 1:
            getPlotSingleVariable(X, chosen[0], chosen[0] in categorical, chosen[0] in continuous, chosen[0] in discreet)
            
        option = getOption("¿Realizar otro gráfico para esta selección?\n1. Sí\n2. No\n", 2)
    
        if option == 2:
            graphingThis = False

    option = getOption("¿Realizar graficar otra selección de variables?\n1. Sí\n2. No\n", 2)
    if option == 2:
        graphing = False
        print("¡Gracias por utilizar el programa!")

        
        


        