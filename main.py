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
import pandas as pd  # Librería para manipulación de datos
import numpy as np  # Librería para operaciones numéricas
import matplotlib.pyplot as plt  # Librería para generación de gráficos
from utils import *  # Importa funciones auxiliares desde utils.py
import sys  # Librería para manipulación del sistema

# Solicita al usuario ingresar la ruta del archivo CSV a analizar
path = input("Ingrese el archivo csv a analizar: ")
# Lee el archivo CSV y lo almacena en un DataFrame
X = readCSV(path)

# Verifica si la lectura del archivo fue exitosa
if type(X) == str:
    print(X)  # Imprime el mensaje de error
    sys.exit()  # Termina la ejecución del programa

# Identifica las variables categóricas, continuas y discretas en el DataFrame
categorical, continuous, discreet = identifyVariables(X)

# Imprime las variables categóricas
print("\nVariables categóricas:")
for i, col in enumerate(categorical, 1):
    print(f"{i}. {col}")

# Imprime las variables numéricas continuas
print("\nVariables numéricas contínuas:")
for i, col in enumerate(continuous, 1):
    print(f"{i}. {col}")

# Imprime las variables numéricas discretas
print("\nVariables numéricas discretas:")
for i, col in enumerate(discreet, 1):
    print(f"{i}. {col}")

# Obtiene las columnas con valores nulos y la cantidad de nulos en cada una
null_values = getNulls(X)

# Verifica si existen valores nulos en el DataFrame
if len(null_values) > 0:
    print("\nEl dataset contiene valores nulos:")
    for t in null_values:
        print(f"La columna '{t[0]}' contiene {t[1]} valores nulos ({t[2]*100:.2f}% del total).")

# Combina las variables continuas y discretas en una sola lista
numerics = continuous + discreet

# Obtiene las estadísticas descriptivas para las variables numéricas
statistics = getStatistics(X, numerics)

# Verifica si existen estadísticas descriptivas para imprimir
if len(statistics) > 0:
    print("\nA continuación, se listan las estadísticas descriptivas para cada variable numérica:")

    for col, st in statistics.items():
        print(f"Variable {col}:")
        print(f"Media: {st[0]}")
        print(f"Mediana: {st[1]}")
        print(f"Moda: {st[2]}")
        print(f"Desviación Estándar: {st[3]}\n")

# Solicita al usuario si desea generar gráficos
option = getOption("¿Desea generar gráficos?\n1. Sí\n2. No\n", 2)

# Si el usuario no desea generar gráficos, termina la ejecución del programa
if option == 2:
    print("¡Gracias por utilizar el programa!")
    sys.exit()

# Variable para controlar el bucle de generación de gráficos
graphing = True

# Bucle principal para la generación de gráficos
while(graphing):

    chosen = []  # Lista para almacenar las variables seleccionadas
    choosing = True  # Variable para controlar el bucle de selección de variables

    # Bucle para la selección de variables
    while choosing:
        # Lista de variables disponibles para seleccionar
        variables = [col for col in list(X.columns) if col not in chosen]
        for i, col in enumerate(variables, 1):
            print(f"{i}. {col}")

        # Solicita al usuario seleccionar una variable
        option = getOption("Seleccione una variable:", len(variables))

        var = variables[option-1]  # Obtiene la variable seleccionada
        chosen.append(var)  # Añade la variable seleccionada a la lista

        # Solicita al usuario si desea seleccionar una variable adicional
        option = getOption("¿Seleccionar variable adicional?\n1. Sí\n2. No\n", 2)

        if option == 2:
            choosing = False  # Termina el bucle de selección de variables

    graphingThis = True  # Variable para controlar el bucle de generación de gráficos para la selección actual

    # Bucle para la generación de gráficos para la selección actual
    while graphingThis:

        # Si solo se seleccionó una variable, genera un gráfico para esa variable
        if len(chosen) == 1:
            getPlotSingleVariable(X, chosen[0], chosen[0] in categorical, chosen[0] in continuous, chosen[0] in discreet)
        # Si se seleccionaron 2 variables, genera un gráfico para esa varaible
        if len (chosen) == 2:
            getPlotTwoVariables(X, chosen[0], chosen[1], categorical, continuous, discreet)

        # Solicita al usuario si desea generar otro gráfico para la selección actual
        option = getOption("¿Realizar otro gráfico para esta selección?\n1. Sí\n2. No\n", 2)

        if option == 2:
            graphingThis = False  # Termina el bucle de generación de gráficos para la selección actual

    # Solicita al usuario si desea generar gráficos para otra selección de variables
    option = getOption("¿Realizar graficar otra selección de variables?\n1. Sí\n2. No\n", 2)
    if option == 2:
        graphing = False  # Termina el bucle principal de generación de gráficos
        print("¡Gracias por utilizar el programa!")  # Mensaje de despedida
        
