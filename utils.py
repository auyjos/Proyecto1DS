import pandas as pd

def getOption(menu, options):
    """
        Muestra un menú y permite seleccionar entre las opciones disponibles, verificando que sea una opción válida
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
        Devuelve una lista de tuplas de la forma (variable, cantidad_nulos)
    """
    nulls = [(col,X.isnull().sum()[col],X.isnull().sum()[col]/X.shape[0]) for col in X.columns]
    nulls = [n for n in nulls if n[1] > 0]
    return nulls

def getStatistics(X, numerics):
    """
    Muestra las estadísticas descriptivas para cada variable numérica en el dataframe X.
    Devuelve un diccionario de la forma:
        col: (media, mediana, moda, desviación estándar)
    
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