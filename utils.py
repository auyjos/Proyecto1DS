import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getOption(menu, options):
    """
        Muestra un menú y permite seleccionar entre las opciones disponibles, verificando que sea una opción válida.
    """
    option = 0
    
    while(True):
        try:
            option = int(input(menu))
            if option <= 0 or option > options:
                print("Opción no válida")
            else:
                break
        except:
            print("Debe ingresar un número entero válido.\n")
    return option

def readCSV(path):
    """
        Recibe la ruta al archivo csv que se desea analizar y valida que este sea válido para el análisis.
    """
    
    try:
        X = pd.read_csv(path)
        
        if X.empty:
            return "El archivo CSV está vacío."
        
        return X

    except FileNotFoundError:
        return f"No se encontró el archivo en la ruta '{path}'."
    except pd.errors.EmptyDataError:
        return "El archivo CSV está vacío."
    except pd.errors.ParserError:
        return "Error al analizar el archivo CSV."
    except ValueError as e:
        return e
    except Exception as e:
        return f"Se produjo un error inesperado: {e}"
    
import pandas as pd

def identifyVariables(X):
    """
    Identifica las variables del dataframe X como:
        Categóricas
        Numéricas Continuas
        Numéricas Discretas
    """
    columnas_continuas = []
    columnas_discretas = []
    columnas_categoricas = []

    for column in X.columns:
        try:
            X[column] = pd.to_numeric(X[column], errors='coerce')
        except:
            columnas_categoricas.append(column)
            continue

        num_unique = X[column].nunique()

        if num_unique <= 2:
            columnas_categoricas.append(column)
        elif X[column].dropna().apply(lambda x: x.is_integer()).all():
            columnas_discretas.append(column)
        else:
            columnas_continuas.append(column)

    return [columnas_categoricas, columnas_continuas, columnas_discretas]

def getNulls(X):
    """
        Para un dataframe dado, identifica las variables en las que existan valores nulos y cuántos hay.
        Devuelve una lista de tuplas de la forma (variable, cantidad_nulos).
    """
    nulls = [(col,X.isnull().sum()[col],X.isnull().sum()[col]/X.shape[0]) for col in X.columns]
    nulls = [n for n in nulls if n[1] > 0]
    return nulls

def getStatistics(X, numerics):
    """
    Muestra las estadísticas descriptivas para cada variable numérica en el dataframe X.
    Devuelve un diccionario de la forma: 
    { var: (media, mediana, moda, desviación estándar) }
    para cada variable.
    """
    statistics = {}
    
    for col in numerics:
        mean = X[col].mean()
        median = X[col].median()
        mode = X[col].mode().values[0] if not X[col].mode().empty else None
        std = X[col].std()
        
        statistics[col] = (mean, median, mode, std)

    return statistics

def getPlotSingleVariable(X, var, categorical=False, continuous=False, discrete=True):
    """
        Permite seleccionar y mostrar el gráfico apropiado según el tipo de variable.
        Versión para una única variable solamente.
    """
    
    types = ["Gráfico de Barras","Gráfico de Torta","Gráfico de Pareto"] \
        if categorical else ["Histograma", "Gráfico de Densidad", "Box Plot"] if continuous \
            else ["Gráfico de Barras", "Histograma", "Gráfico de Pareto", "Box Plot"]
            
    for i, graph in enumerate(types, 1):
        print(f"{i}. {graph}")
    option = getOption("Seleccione una tipo de gráfico:",len(types))
    
    chosen = types[option-1]
    
    if chosen == "Gráfico de Barras":
        frequency = X[var].value_counts()
        
        plt.figure(figsize=(10, 6))
        plt.bar(frequency.index, frequency.values, color='skyblue')

        plt.title(f'Frecuencia de variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')

        plt.xticks(rotation=45, ha='right')

        plt.show()
    elif chosen == "Histograma":
        plt.figure(figsize=(10, 6))
        plt.hist(X[var], bins=10, color='skyblue', edgecolor='black')

        plt.title(f'Histograma para variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')

        plt.show()
    elif chosen == "Gráfico de Pareto":
        frequency = X[var].value_counts()
        frequency = frequency.sort_values(ascending=False)
        
        porcentaje_acumulado = frequency.cumsum() / frequency.sum() * 100

        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        ax1.bar(frequency.index.astype(str), frequency, color='skyblue', edgecolor='black')
        ax1.set_xlabel(var)
        ax1.set_ylabel('Frecuencia', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')

        ax2 = ax1.twinx()
        ax2.plot(frequency.index.astype(str), porcentaje_acumulado, color='red', marker='o', linestyle='--')
        ax2.set_ylabel('Porcentaje Acumulado (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        plt.title(f'Gráfico de Pareto para {var}')
        plt.show()
    elif chosen == "Box Plot":
        plt.figure(figsize=(10, 6))
        plt.boxplot(X[var].dropna(), vert=False, patch_artist=True,
            boxprops=dict(facecolor='skyblue', color='black'),
            whiskerprops=dict(color='black'),
            capprops=dict(color='black'),
            medianprops=dict(color='red'))
        
        plt.title(f'Box Plot para {var}')
        plt.xlabel(var)
        
        plt.show()
        
    elif chosen == "Gráfico de Torta":
        frequency = X[var].value_counts()
        
        plt.figure(figsize=(8, 8))
        plt.pie(frequency, labels=frequency.index, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(frequency))))

        plt.title(f'Gráfico de Torta para {var}')
        plt.show()
    
    elif chosen == "Gráfico de Densidad":
        plt.figure(figsize=(10, 6))
        sns.kdeplot(X[var].dropna(), fill=True, color='skyblue')
        
        plt.title(f'Gráfico de Densidad para {var}')
        plt.xlabel(var)
        plt.ylabel('Densidad')
        plt.show()