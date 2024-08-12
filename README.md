# Proyecto1DS

## Descripción
Este proyecto realiza un Análisis Exploratorio de Datos (EDA) de un archivo CSV o Excel proporcionado por el usuario. Permite cargar el archivo, identificar variables categóricas y numéricas, detectar valores nulos y generar gráficos para visualizar los datos.

## Requisitos
- Python 3.x
- Librerías: `pandas`, `numpy`, `matplotlib`, `seaborn`, `tkinter`

## Instalación
1. Clona el repositorio:
    ```sh
    git clone git@github.com:auyjos/Proyecto1DS.git
    ```
2. Instala las dependencias:
    ```sh
    pip install pandas numpy matplotlib seaborn
    ```

## Uso en consola
1. Ejecuta el archivo `main.py` para iniciar el análisis de datos:
    ```sh
    python main.py
    ```
2. Sigue las instrucciones en la consola para cargar el archivo CSV y realizar el análisis.

## Uso en interfaz gráfica
1. Ejecuta el archivo `gui.py` para iniciar el análisis de datos:
    ```sh
    python main.py
    ```
## Funciones Principales

### `interfaz.py`
- `load_file()`: Abre un cuadro de diálogo para seleccionar un archivo CSV o Excel y carga los datos en un DataFrame de pandas.

### `gui.py`
- `CollapsibleFrame`: Clase que permite instanciar un elemento colapsable dentro de la ventana.


### `utils.py`
- `getOption(menu, options)`: Muestra un menú y permite seleccionar entre las opciones disponibles, verificando que sea una opción válida.
- `readCSV(path)`: Recibe la ruta al archivo CSV que se desea analizar y valida que este sea válido para el análisis.
- `identifyVariables(X)`: Identifica las variables del DataFrame `X` como categóricas, numéricas continuas y numéricas discretas.
- `getNulls(X)`: Identifica las variables en las que existen valores nulos y cuántos hay.
- `getStatistics(X, numerics)`: Muestra las estadísticas descriptivas para cada variable numérica en el DataFrame `X`.
- `getPlotSingleVariable(X, var, categorical=False, continuous=False, discrete=True)`: Permite seleccionar y mostrar el gráfico apropiado según el tipo de variable.
- `getPlotTwoVariables(X, var1, var2, categorical, continuous, discreet)`: Permite seleccionar y mostrar el gráfico apropiado según el tipo de variables para dos variables.

### `main.py`
- Ejecuta el flujo principal del programa, solicitando al usuario que ingrese el archivo CSV, identificando las variables, mostrando estadísticas descriptivas y generando gráficos.

## Autores
- Herber Sebastián Silva Muñoz
- Eunice Anahí Mata Ixcayau
- José Andrés Auyón Cóbar
- Erick Stiv Junior Guerra Muñoz
