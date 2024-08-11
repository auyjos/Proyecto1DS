import pandas as pd
from tkinter import simpledialog, messagebox, Tk, Button, scrolledtext
from utils import identifyVariables, getPlotSingleVariable, getPlotTwoVariables, getNulls, getStatistics
import sys


def show_eda_results(X, categorical, continuous, discreet):
    def generate_graphs_action():
        root.destroy()
        generate_graphs(X, categorical, continuous, discreet)

    def close_program():
        root.destroy()
        sys.exit()

    # Crear la ventana principal
    root = Tk()
    root.title("Resultados del EDA")

    # Crear un widget Text con barra de desplazamiento
    text_area = scrolledtext.ScrolledText(root, width=100, height=30)
    text_area.pack(padx=10, pady=10)

    # Desactivar la edición del Text widget
    text_area.config(state='disabled')

    # Obtener y mostrar las variables
    
    vars_str = ""
    
    if len(categorical) > 0:
        vars_str += "\nVariables categóricas:\n" + \
            "\n".join([f"{i+1}. {col}" for i, col in enumerate(categorical)])
    if len(continuous) > 0:
        vars_str += "\n\nVariables continuas:\n" + \
            "\n".join([f"{i+1}. {col}" for i, col in enumerate(continuous)])
    if len(discreet) > 0:
        vars_str += "\n\nVariables discretas:\n" + \
            "\n".join([f"{i+1}. {col}" for i, col in enumerate(discreet)])

    # Mostrar variables en el Text widget
    text_area.config(state='normal')
    text_area.insert('end', "Información de Variables:\n")
    text_area.insert('end', vars_str + "\n\n")

    # Obtener y mostrar valores nulos
    null_values = getNulls(X)
    if len(null_values) > 0:
        nulls_str = "\n".join([f"La columna '{t[0]}' contiene {t[1]} valores nulos ({
                              t[2]*100:.2f}% del total)." for t in null_values])
        text_area.insert('end', "Valores Nulos:\n")
        text_area.insert(
            'end', f"El conjunto de datos contiene valores nulos:\n{nulls_str}\n\n")

    # Obtener y mostrar estadísticas descriptivas
    numerics = continuous + discreet
    statistics = getStatistics(X, numerics)
    if len(statistics) > 0:
        stats_str = "\n".join([f"Variable {col}:\n Media: {st[0]}\n Mediana: {st[1]}\n Moda: {
                              st[2]}\n Desviación Estándar: {st[3]}\n" for col, st in statistics.items()])
        text_area.insert('end', "Estadísticas Descriptivas:\n")
        text_area.insert(
            'end', f"Estadísticas descriptivas para variables numéricas:\n{stats_str}\n")

    # Agregar botones para generar gráficos y cerrar el programa
    Button(root, text="Generar Gráficos",
           command=generate_graphs_action).pack(pady=10)
    Button(root, text="Cerrar Programa", command=close_program).pack(pady=10)

    # Mostrar la ventana principal
    root.mainloop()


def generate_graphs(X, categorical, continuous, discreet):
    def handle_variable_selection():
        chosen = []
        max_chosen = 2
        while True:
            
            variables = [col for col in X.columns if col not in chosen]
            vars_str = "\n".join(
                [f"{i+1}. {col}" for i, col in enumerate(variables)])
            option = simpledialog.askinteger("Seleccionar Variable", f"Selecciona una variable:\n{vars_str}", minvalue=1, maxvalue=len(variables))

            if option is None:
                messagebox.showwarning(
                    "Selección Cancelada", "No se seleccionó ninguna variable.")
                continue

            if 1 <= option <= len(variables):
                max_chosen -= 1
                var = variables[option - 1]
                chosen.append(var)
            else:
                messagebox.showwarning(
                    "Selección Inválida", "La opción seleccionada no es válida.")
                continue
            
            if max_chosen <= 0:
                break

            option = simpledialog.askinteger(
                "Seleccionar Variable Adicional", "¿Seleccionar otra variable?\n1. Sí\n2. No", minvalue=1, maxvalue=2)

            if option is None:
                messagebox.showwarning(
                    "Selección Cancelada", "No se seleccionó ninguna opción.")
                continue

            if option == 2:
                break

        return chosen

    while True:
        option = simpledialog.askinteger(
            "Generar Gráficos", "¿Desea generar gráficos?\n1. Sí\n2. No", minvalue=1, maxvalue=2)

        if option is None:
            messagebox.showwarning("Selección Cancelada",
                                   "No se seleccionó ninguna opción.")
            continue

        if option == 2:
            messagebox.showinfo("Gracias", "¡Gracias por usar el programa!")
            sys.exit()

        chosen = handle_variable_selection()

        # Generar gráficos
        while True:
            if len(chosen) == 1:
                getPlotSingleVariable(
                    X, chosen[0], chosen[0] in categorical, chosen[0] in continuous, chosen[0] in discreet)
            elif len(chosen) == 2:
                getPlotTwoVariables(
                    X, chosen[0], chosen[1], categorical, continuous, discreet)

            option = simpledialog.askinteger(
                "Generar Otro Gráfico", "¿Generar otro gráfico para esta selección?\n1. Sí\n2. No", minvalue=1, maxvalue=2)

            if option is None:
                messagebox.showwarning(
                    "Selección Cancelada", "No se seleccionó ninguna opción.")
                continue

            if option == 2:
                break

        option = simpledialog.askinteger(
            "Generar Otra Selección", "¿Generar gráficos para otra selección de variables?\n1. Sí\n2. No", minvalue=1, maxvalue=2)

        if option is None:
            messagebox.showwarning("Selección Cancelada",
                                   "No se seleccionó ninguna opción.")
            continue

        if option == 2:
            messagebox.showinfo("Gracias", "¡Gracias por usar el programa!")
            sys.exit()


def analyze_data(X):
    categorical, continuous, discreet = identifyVariables(X.copy())
    show_eda_results(X, categorical, continuous, discreet)
