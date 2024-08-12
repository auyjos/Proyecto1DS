import pandas as pd  # Importa pandas para manipulación de datos
import matplotlib.pyplot as plt  # Importa matplotlib para generación de gráficos
import seaborn as sns  # Importa seaborn para gráficos estadísticos
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, simpledialog
import matplotlib.backends.backend_tkagg as tkagg


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

    while (True):  # Bucle infinito hasta que se seleccione una opción válida
        try:
            # Solicita al usuario ingresar una opción
            option = int(input(menu))
            # Verifica si la opción ingresada es válida
            if option <= 0 or option > options:
                # Mensaje de error para opción no válida
                print("Opción no válida")
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


def identifyVariables(dataset):
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
    X = dataset.copy()
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
    nulls = [(col, X.isnull().sum()[col], X.isnull().sum()
              [col] / X.shape[0]) for col in X.columns]
    # Filtra las columnas que tienen al menos un valor nulo
    # nulls = [n for n in nulls if n[1] > 0]
    nulls = {col: [count, percentage] for col, count, percentage in nulls if count > 0}
    return nulls  # Retorna el diccionario


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
        # Intentar convertir la columna a valores numéricos, forzando a NaN los valores no convertibles
        X[col] = pd.to_numeric(X[col], errors='coerce')
        
        # Elimina filas con NaN en la columna actual
        X_cleaned = X[col].dropna()
        
        # Calcula estadísticas si la columna no está vacía
        if not X_cleaned.empty:
            mean = X_cleaned.mean()  # Calcula la media
            median = X_cleaned.median()  # Calcula la mediana
            mode = X_cleaned.mode().values[0] if not X_cleaned.mode().empty else None  # Calcula la moda
            std = X_cleaned.std()  # Calcula la desviación estándar

            # Almacena las estadísticas en el diccionario
            statistics[col] = (mean, median, mode, std)
        else:
            statistics[col] = (None, None, None, None)

    return statistics  # Retorna el diccionario con las estadísticas

def getPlotSingleVariableTypes(varType):
    """
    Devuelve los tipos de gráficos disponibles para una única variable.
    Arg:
        varType (str): El tipo de variable a graficar (CAT | CONT | DISC).
    """

    # Define los tipos de gráficos disponibles según el tipo de variable
    if varType == "CAT":
        return ["Gráfico de Barras", "Gráfico de Torta", "Gráfico de Pareto"]
    elif varType == "CONT":
        return ["Histograma", "Gráfico de Densidad", "Box Plot"]
    else:  # Si es discreta
        return ["Gráfico de Barras", "Histograma",
                 "Gráfico de Pareto", "Box Plot"]
        
def getPlotByType(type, X, var, font_size):
    """
    Devuelve el gráfico generado según el tipo indicado.
    Args:
        type (str): El tipo de gráfico a crear.
        X (dataFrame): DataFrame con los datos.
        var (str): Nombre de la columna en X para graficar.
    """
    fig, ax = plt.subplots(figsize=(4,3))

    if type == "Gráfico de Barras":
        frequency = X[var].value_counts()
        ax.bar(frequency.index, frequency.values, color='skyblue')
        ax.set_title(f'Frecuencia de la variable {var}')
        ax.set_xlabel(var)
        ax.set_ylabel('Frecuencia')
        ax.tick_params(axis='x', rotation=45)

    elif type == "Histograma":
        ax.hist(X[var], bins=10, color='skyblue', edgecolor='black')
        ax.set_title(f'Histograma de la variable {var}')
        ax.set_xlabel(var)
        ax.set_ylabel('Frecuencia')

    elif type == "Gráfico de Pareto":
        frequency = X[var].value_counts()
        frequency = frequency.sort_values(ascending=False)
        porcentaje_acumulado = frequency.cumsum() / frequency.sum() * 100
        fig, ax1 = plt.subplots(figsize=(4,3))
        ax1.bar(frequency.index.astype(str), frequency,
                color='skyblue', edgecolor='black')
        ax1.set_xlabel(var)
        ax1.set_ylabel('Frecuencia', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(frequency.index.astype(str), porcentaje_acumulado,
                 color='red', marker='o', linestyle='--')
        ax2.set_ylabel('Porcentaje Acumulado (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Gráfico de Pareto de la variable {var}')
        ax1.title.set_fontsize(font_size)
        ax1.xaxis.label.set_fontsize(font_size)
        ax1.yaxis.label.set_fontsize(font_size)
        ax1.tick_params(axis='both', which='major', labelsize=font_size)
        ax2.title.set_fontsize(font_size)
        ax2.xaxis.label.set_fontsize(font_size)
        ax2.yaxis.label.set_fontsize(font_size)
        ax2.tick_params(axis='both', which='major', labelsize=font_size)

    elif type == "Box Plot":
        ax.boxplot(X[var].dropna(), vert=False, patch_artist=True,
                    boxprops=dict(facecolor='skyblue', color='black'),
                    whiskerprops=dict(color='black'),
                    capprops=dict(color='black'),
                    medianprops=dict(color='red'))
        ax.set_title(f'Box Plot de la variable {var}')
        ax.set_xlabel(var)

    elif type == "Gráfico de Torta":
        frequency = X[var].value_counts()
        ax.pie(frequency, labels=frequency.index, autopct='%1.1f%%',
               colors=plt.cm.Paired(range(len(frequency))))
        ax.set_title(f'Gráfico de Torta de la variable {var}')

    elif type == "Gráfico de Densidad":
        sns.kdeplot(X[var].dropna(), fill=True, color='skyblue', ax=ax)
        ax.set_title(f'Gráfico de Densidad de la variable {var}')
        ax.set_xlabel(var)
        ax.set_ylabel('Densidad')

    return fig, ax

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
    if categorical:
        types = ["Gráfico de Barras", "Gráfico de Torta", "Gráfico de Pareto"]
    elif continuous:
        types = ["Histograma", "Gráfico de Densidad", "Box Plot"]
    else:  # Si es discreta
        types = ["Gráfico de Barras", "Histograma",
                 "Gráfico de Pareto", "Box Plot"]

    # Solicita al usuario seleccionar el tipo de gráfico
    chosen = simpledialog.askstring(
        "Seleccionar Tipo de Gráfico",
        "Seleccione el tipo de gráfico:\n" +
        "\n".join([f"{i+1}. {t}" for i, t in enumerate(types)]),
        initialvalue="1"
    )

    if not chosen or not chosen.isdigit() or int(chosen) not in range(1, len(types) + 1):
        messagebox.showerror(
            "Opción Inválida", "La opción seleccionada no es válida.")
        return

    chosen = types[int(chosen) - 1]  # Obtiene el tipo de gráfico seleccionado

    # Crea una figura para el gráfico
    plt.figure(figsize=(10, 6))

    # Genera el gráfico seleccionado
    if chosen == "Gráfico de Barras":
        frequency = X[var].value_counts()
        plt.bar(frequency.index, frequency.values, color='skyblue')
        plt.title(f'Frecuencia de la variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45, ha='right')

    elif chosen == "Histograma":
        plt.hist(X[var], bins=10, color='skyblue', edgecolor='black')
        plt.title(f'Histograma de la variable {var}')
        plt.xlabel(var)
        plt.ylabel('Frecuencia')

    elif chosen == "Gráfico de Pareto":
        frequency = X[var].value_counts()
        frequency = frequency.sort_values(ascending=False)
        porcentaje_acumulado = frequency.cumsum() / frequency.sum() * 100
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(frequency.index.astype(str), frequency,
                color='skyblue', edgecolor='black')
        ax1.set_xlabel(var)
        ax1.set_ylabel('Frecuencia', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(frequency.index.astype(str), porcentaje_acumulado,
                 color='red', marker='o', linestyle='--')
        ax2.set_ylabel('Porcentaje Acumulado (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Gráfico de Pareto de la variable {var}')

    elif chosen == "Box Plot":
        plt.boxplot(X[var].dropna(), vert=False, patch_artist=True,
                    boxprops=dict(facecolor='skyblue', color='black'),
                    whiskerprops=dict(color='black'),
                    capprops=dict(color='black'),
                    medianprops=dict(color='red'))
        plt.title(f'Box Plot de la variable {var}')
        plt.xlabel(var)

    elif chosen == "Gráfico de Torta":
        frequency = X[var].value_counts()
        plt.pie(frequency, labels=frequency.index, autopct='%1.1f%%',
                colors=plt.cm.Paired(range(len(frequency))))
        plt.title(f'Gráfico de Torta de la variable {var}')

    elif chosen == "Gráfico de Densidad":
        sns.kdeplot(X[var].dropna(), fill=True, color='skyblue')
        plt.title(f'Gráfico de Densidad de la variable {var}')
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

    if var1 not in X.columns or var2 not in X.columns:
        messagebox.showerror("Error", f"Las variables {var1} o {
                             var2} no están en el DataFrame")
        return

    # Determina el tipo de cada variable
    var1_cat = var1 in categorical
    var1_cont = var1 in continuous
    var1_disc = var1 in discreet

    var2_cat = var2 in categorical
    var2_cont = var2 in continuous
    var2_disc = var2 in discreet

    # Crear ventana para selección de variables y gráficos
    root = Tk()
    root.title("Seleccionar Variables")

    # Mostrar variables disponibles
    variables_str = f"Variables disponibles:\n1. {var1}\n2. {var2}"
    label = Label(root, text=variables_str, padx=10, pady=10)
    label.pack()
    additional_text = "La variable escogida se mostrará en el eje X"
    label_additional = Label(root, text=additional_text, padx=10, pady=10)
    label_additional.pack()

    # Variable para el eje X
    var_x_var = StringVar()
    var_x_entry = Entry(root, textvariable=var_x_var, width=50)
    var_x_entry.pack(padx=10, pady=10)
    var_x_var.set(variables_str.split("\n")[1].split(
        ". ")[1])  # Pre-set the first variable

    def on_select_variable():
        var_x = var_x_var.get()
        if var_x not in [var1, var2]:
            messagebox.showerror(
                "Variable Inválida", "La variable seleccionada no está en el DataFrame.")
            return

        var_y = var1 if var_x == var2 else var2

        # Define los tipos de gráficos disponibles según el tipo de variables
        if var1_cat and var2_cat:
            types = ["Gráfico de Contingencia"]
        elif var1_cont and var2_cont:
            types = ["Gráfico de Dispersión", "Gráfico de Densidad 2D"]
        elif (var1_cat and (var2_cont or var2_disc)) or (var2_cat and (var1_cont or var1_disc)):
            types = ["Gráfico de Cajas", "Gráfico de Violin"]
        elif var1_disc and var2_disc:
            types = ["Gráfico de Dispersión"]

        # Solicita al usuario seleccionar el tipo de gráfico
        options_str = "\n".join([f"{i+1}. {t}" for i, t in enumerate(types)])
        chosen_index = simpledialog.askinteger("Seleccionar Tipo de Gráfico", f"Gráficos disponibles:\n{
                                               options_str}", minvalue=1, maxvalue=len(types))

        if not chosen_index:
            messagebox.showerror(
                "Opción Inválida", "La opción seleccionada no es válida.")
            return

        # Obtiene el tipo de gráfico seleccionado
        chosen = types[chosen_index - 1]

        # Crea una figura para el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))

        # Genera el gráfico seleccionado
        if chosen == "Gráfico de Contingencia":
            contingency_table = pd.crosstab(X[var_x], X[var_y])
            sns.heatmap(contingency_table, annot=True,
                        fmt="d", cmap="YlGnBu", ax=ax)
            ax.set_title(f'Gráfico de Contingencia entre {var_x} y {var_y}')
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)

        elif chosen == "Gráfico de Dispersión":
            ax.scatter(X[var_x], X[var_y], alpha=0.5)
            ax.set_title(f'Gráfico de Dispersión entre {var_x} y {var_y}')
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)

        elif chosen == "Gráfico de Densidad 2D":
            sns.kdeplot(x=X[var_x], y=X[var_y],
                        cmap="Blues", shade=True, ax=ax)
            ax.set_title(f'Gráfico de Densidad 2D entre {var_x} y {var_y}')
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)

        elif chosen == "Gráfico de Cajas":
            sns.boxplot(x=X[var_x], y=X[var_y], ax=ax)
            ax.set_title(f'Gráfico de Cajas entre {var_x} y {var_y}')
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)

        elif chosen == "Gráfico de Violin":
            sns.violinplot(x=X[var_x], y=X[var_y], ax=ax)
            ax.set_title(f'Gráfico de Violin entre {var_x} y {var_y}')
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)

        # Muestra el gráfico en la interfaz gráfica
        plt.show()
        root.destroy()

    # Botón para confirmar selección
    select_button = Button(root, text="Generar Gráfico",
                           command=on_select_variable)
    select_button.pack(pady=10)

    # Iniciar la ventana
    root.mainloop()
