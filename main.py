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


    