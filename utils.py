import pandas as pd  # Importa pandas para manipulación de datos
import matplotlib.pyplot as plt  # Importa matplotlib para generación de gráficos
import seaborn as sns  # Importa seaborn para gráficos estadísticos

def getOption(menu, options):
    """
    Muestra un menú y permite seleccionar entre las opciones disponibles, verificando que sea una opción válida.

    Args:
        menu (str): El menú a mostrar al usuario.
        options (int): El número de opciones disponibles en el menú.

    Returns:
        int: La opción seleccionada por el usuario.
    """
    option = 0  # Inicializa la variable para almacenar la opción seleccionada
    
    while(True):  # Bucle infinito hasta que se seleccione una opción válida
        try:
            # Solicita al usuario ingresar una opción
            option = int(input(menu))
            # Verifica si la opción ingresada es válida
            if option <= 0 or option > options:
                print("Opción no válida")  # Mensaje de error para opción no válida
            else:
                break  # Sale del bucle si la opción es válida
        except:
            # Mensaje de error para entrada no válida (no es un número entero)
            print("Debe ingresar un número entero válido.\n")
    return option  # Retorna la opción seleccionada

def readCSV(path):
    """
    Recibe la ruta al archivo CSV que se desea analizar y valida que este sea válido para el análisis.

    Args:
        path (str): La ruta al archivo CSV.

    Returns:
        DataFrame o str: Retorna el DataFrame si la lectura es exitosa, de lo contrario, retorna un mensaje de error.
    """
    try:
        # Intenta leer el archivo CSV en un DataFrame
        X = pd.read_csv(path)
        
        # Verifica si el DataFrame está vacío
        if X.empty:
            return "El archivo CSV está vacío."
        
        return X  # Retorna el DataFrame si la lectura es exitosa

    except FileNotFoundError:
        # Retorna un mensaje de error si el archivo no se encuentra en la ruta especificada
        return f"No se encontró el archivo en la ruta '{path}'."
    except pd.errors.EmptyDataError:
        # Retorna un mensaje de error si el archivo CSV está vacío
        return "El archivo CSV está vacío."
    except pd.errors.ParserError:
        # Retorna un mensaje de error si ocurre un problema al analizar el archivo CSV
        return "Error al analizar el archivo CSV."
    except ValueError as e:
        # Retorna el mensaje de error específico si ocurre un ValueError
        return e
    except Exception as e:
        # Retorna un mensaje de error genérico para cualquier otra excepción
        return f"Se produjo un error inesperado: {e}"
    

def identifyVariables(X):
    """
    Identifica las variables del DataFrame X como:
        - Categóricas
        - Numéricas Continuas
        - Numéricas Discretas

    Args:
        X (DataFrame): El DataFrame a analizar.

    Returns:
        list: Una lista de tres listas que contienen los nombres de las columnas categóricas, continuas y discretas.
    """
    columnas_continuas = []  # Lista para almacenar las columnas numéricas continuas
    columnas_discretas = []  # Lista para almacenar las columnas numéricas discretas
    columnas_categoricas = []  # Lista para almacenar las columnas categóricas

    # Itera sobre cada columna del DataFrame
    for column in X.columns:
        try:
            # Intenta convertir la columna a valores numéricos
            X[column] = pd.to_numeric(X[column], errors='coerce')
        except:
            # Si falla, se considera una columna categórica
            columnas_categoricas.append(column)
            continue

        # Cuenta el número de valores únicos en la columna
        num_unique = X[column].nunique()

        if num_unique <= 2:
            # Si hay 2 o menos valores únicos, se considera categórica
            columnas_categoricas.append(column)
        elif X[column].dropna().apply(lambda x: x.is_integer()).all():
            # Si todos los valores son enteros, se considera discreta
            columnas_discretas.append(column)
        else:
            # De lo contrario, se considera continua
            columnas_continuas.append(column)

    # Retorna las listas de columnas categóricas, continuas y discretas
    return [columnas_categoricas, columnas_continuas, columnas_discretas]

def getNulls(X):
    """
    Para un DataFrame dado, identifica las variables en las que existan valores nulos y cuántos hay.

    Args:
        X (DataFrame): El DataFrame a analizar.

    Returns:
        list: Una lista de tuplas de la forma (variable, cantidad_nulos, porcentaje_nulos).
    """
    # Crea una lista de tuplas con el nombre de la columna, la cantidad de nulos y el porcentaje de nulos
    nulls = [(col, X.isnull().sum()[col], X.isnull().sum()[col] / X.shape[0]) for col in X.columns]
    # Filtra las columnas que tienen al menos un valor nulo
    nulls = [n for n in nulls if n[1] > 0]
    return nulls  # Retorna la lista de tuplas

def getStatistics(X, numerics):
    """
    Muestra las estadísticas descriptivas para cada variable numérica en el dataframe X.
    Devuelve un diccionario de la forma: 
    { var: (media, mediana, moda, desviación estándar) }
    para cada variable.

    Args:
        X (DataFrame): El DataFrame a analizar.
        numerics (list): Lista de nombres de columnas numéricas.

    Returns:
        dict: Diccionario con estadísticas descriptivas para cada variable numérica.
    """
    statistics = {}  # Diccionario para almacenar las estadísticas
    
    # Itera sobre cada columna numérica
    for col in numerics:
        mean = X[col].mean()  # Calcula la media
        median = X[col].median()  # Calcula la mediana
        mode = X[col].mode().values[0] if not X[col].mode().empty else None  # Calcula la moda
        std = X[col].std()  # Calcula la desviación estándar
        
        # Almacena las estadísticas en el diccionario
        statistics[col] = (mean, median, mode, std)

    return statistics  # Retorna el diccionario con las estadísticas


def getPlotSingleVariable(X, var, categorical=False, continuous=False, discrete=True):
    """
    Permite seleccionar y mostrar el gráfico apropiado según el tipo de variable.
    Versión para una única variable solamente.

    Args:
        X (DataFrame): El DataFrame a analizar.
        var (str): El nombre de la variable a graficar.
        categorical (bool): Indica si la variable es categórica.
        continuous (bool): Indica si la variable es continua.
        discrete (bool): Indica si la variable es discreta.
    """
    
    # Define los tipos de gráficos disponibles según el tipo de variable
    types = ["Gráfico de Barras","Gráfico de Torta","Gráfico de Pareto"] \
        if categorical else ["Histograma", "Gráfico de Densidad", "Box Plot"] if continuous \
            else ["Gráfico de Barras", "Histograma", "Gráfico de Pareto", "Box Plot"]
    
    # Muestra las opciones de gráficos disponibles
    for i, graph in enumerate(types, 1):
        print(f"{i}. {graph}")
    
    # Solicita al usuario seleccionar un tipo de gráfico
    option = getOption("Seleccione una tipo de gráfico:", len(types))
    
    chosen = types[option-1]  # Obtiene el tipo de gráfico seleccionado
    
    if chosen == "Gráfico de Barras":
        # Genera un gráfico de barras
        frequency = X[var].value_counts()
        
        plt.figure(figsize=(10, 6))
        plt.bar(frequency.index, frequency.values, color='skyblue')

        plt.title(f'Frecuencia de variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')

        plt.xticks(rotation=45, ha='right')

        plt.show()
    elif chosen == "Histograma":
        # Genera un histograma
        plt.figure(figsize=(10, 6))
        plt.hist(X[var], bins=10, color='skyblue', edgecolor='black')

        plt.title(f'Histograma para variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')

        plt.show()
    elif chosen == "Gráfico de Pareto":
        # Genera un gráfico de Pareto
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
        # Genera un box plot
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
        # Genera un gráfico de torta
        frequency = X[var].value_counts()
        
        plt.figure(figsize=(8, 8))
        plt.pie(frequency, labels=frequency.index, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(frequency))))

        plt.title(f'Gráfico de Torta para {var}')
        plt.show()
    
    elif chosen == "Gráfico de Densidad":
        # Genera un gráfico de densidad
        plt.figure(figsize=(10, 6))
        sns.kdeplot(X[var].dropna(), fill=True, color='skyblue')
        
        plt.title(f'Gráfico de Densidad para {var}')
        plt.xlabel(var)
        plt.ylabel('Densidad')
        plt.show()


def getPlotTwoVariables(X, var1, var2, categorical, continuous, discreet):
    """
    Permite seleccionar y mostrar el gráfico apropiado según el tipo de variables.
    Versión para dos variables.

    Args:
        X (DataFrame): El DataFrame a analizar.
        var1 (str): El nombre de la primera variable.
        var2 (str): El nombre de la segunda variable.
        categorical (list): Lista de nombres de columnas categóricas.
        continuous (list): Lista de nombres de columnas continuas.
        discreet (list): Lista de nombres de columnas discretas.
    """
    
    print(f"Variables seleccionadas: {var1} y {var2}")
    
    # Determina el tipo de cada variable
    var1_cat = var1 in categorical
    var1_cont = var1 in continuous
    var1_disc = var1 in discreet

    var2_cat = var2 in categorical
    var2_cont = var2 in continuous
    var2_disc = var2 in discreet
    
    # Solicita al usuario seleccionar la variable para el eje X
    print("Seleccione la variable para el eje X:")
    print(f"1. {var1}")
    print(f"2. {var2}")
    option = getOption("Opción:", 2)
    
    if option == 1:
        x_var = var1
        y_var = var2
    else:
        x_var = var2
        y_var = var1
    
    # Define los tipos de gráficos disponibles según el tipo de variables
    if var1_cat and var2_cat:
        types = ["Gráfico de Contingencia"]
    elif var1_cont and var2_cont:
        types = ["Gráfico de Dispersión", "Gráfico de Densidad 2D"]
    elif (var1_cat and (var2_cont or var2_disc)) or (var2_cat and (var1_cont or var1_disc)):
        types = ["Gráfico de Cajas", "Gráfico de Violin"]
    elif var1_disc and var2_disc:
        types = ["Gráfico de Dispersión"]
    
    # Muestra las opciones de gráficos disponibles
    for i, graph in enumerate(types, 1):
        print(f"{i}. {graph}")
    option = getOption("Seleccione un tipo de gráfico:", len(types))
    
    chosen = types[option-1]  # Obtiene el tipo de gráfico seleccionado
    
    # Genera el gráfico seleccionado
    if chosen == "Gráfico de Contingencia":
        # Genera un gráfico de contingencia
        contingency_table = pd.crosstab(X[x_var], X[y_var])
        sns.heatmap(contingency_table, annot=True, fmt="d", cmap="YlGnBu")
        plt.title(f'Gráfico de Contingencia entre {x_var} y {y_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()
        
    elif chosen == "Gráfico de Dispersión":
        # Genera un gráfico de dispersión
        plt.figure(figsize=(10, 6))
        plt.scatter(X[x_var], X[y_var], alpha=0.5)
        plt.title(f'Gráfico de Dispersión entre {x_var} y {y_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()
    
    elif chosen == "Gráfico de Densidad 2D":
        # Genera un gráfico de densidad 2D
        plt.figure(figsize=(10, 6))
        sns.kdeplot(x=X[x_var], y=X[y_var], cmap="Blues", shade=True)
        plt.title(f'Gráfico de Densidad 2D entre {x_var} y {y_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()
    
    elif chosen == "Gráfico de Cajas":
        # Genera un gráfico de cajas
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=X[x_var], y=X[y_var])
        plt.title(f'Gráfico de Cajas entre {x_var} y {y_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()
    
    elif chosen == "Gráfico de Violin":
        # Genera un gráfico de violín
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=X[x_var], y=X[y_var])
        plt.title(f'Gráfico de Violin entre {x_var} y {y_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()