import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from utils import *

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._visible = False
        self._title = title

        self.header = ttk.Frame(self)
        self.toggle_button = ttk.Button(self.header, text=self._title, command=self.toggle)
        self.toggle_button.pack(fill='x')
        self.header.pack(fill='x')

        self.content = ttk.Frame(self)
        self.content.pack_forget()
        
        self.content_grid = ttk.Frame(self.content)
        self.content_grid.pack(fill="both", expand=True)
        
        self.stats_frame = ttk.Frame(self.content_grid)
        self.stats_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.button_frame = ttk.Frame(self.content_grid)
        self.button_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.content_grid.grid_columnconfigure(0, weight=1)
        self.content_grid.grid_columnconfigure(1, weight=2) 
        self.content_grid.grid_rowconfigure(0, weight=1)

        self.graph_type = tk.StringVar(value="Gráfico de Barras")
        self.data = None  
        self.variable = None  

    def toggle(self):
        if self._visible:
            self.content.pack_forget()
            self.toggle_button.config(text=self._title)
        else:
            self.content.pack(fill='x')
            self.toggle_button.config(text=self._title)
        self._visible = not self._visible

    def add_statistics(self, n, st, data, variable, varType):
        self.data = data
        self.variable = variable

        labels = ["Media:", "Mediana:", "Moda:", "Desviación estándar:", "Valores nulos"]
        values = [f"{st[0]}",
                  f"{st[1]}",
                  f"{st[2]}",
                  f"{st[3]}\n",
                  f"{n[0]} ({n[1]*100:.2f}% del total)."]
        for row, (label, value) in enumerate(zip(labels, values)):
            ttk.Label(self.stats_frame, text=label).grid(row=row, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(self.stats_frame, text=value).grid(row=row, column=1, sticky='w', padx=5, pady=2)

        self.graph_menu = ttk.Combobox(self.button_frame, values=getPlotSingleVariableTypes(varType), textvariable=self.graph_type, state='readonly')
        self.graph_menu.pack(pady=5)
        
        self.graph_button = ttk.Button(self.button_frame, text="Generar gráfico", command=self.generate_graph)
        self.graph_button.pack(pady=10)
        
    def generate_graph(self):
        graph_type = self.graph_type.get()

        font_size = 8  

        if self.data is not None and self.variable is not None:
            fig, ax = getPlotByType(graph_type, self.data, self.variable, font_size)
        else:
            fig, ax = plt.subplots(figsize=(4,3))
            ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', fontsize=font_size)
            ax.set_title('Error', fontsize=font_size)
        
        ax.title.set_fontsize(font_size)
        ax.xaxis.label.set_fontsize(font_size)
        ax.yaxis.label.set_fontsize(font_size)
        ax.tick_params(axis='both', which='major', labelsize=font_size)
        
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.button_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

def create_tab_content(parent, collapsibles, nulls, statistics, data, varType):
    collapsibles_container = ttk.Frame(parent)
    
    canvas = tk.Canvas(collapsibles_container)
    scrollbar = ttk.Scrollbar(collapsibles_container, orient="vertical", command=canvas.yview)
    
    tab_content = ttk.Frame(canvas)
    tab_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=tab_content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    for i in range(len(collapsibles)):
        collapsible = CollapsibleFrame(tab_content, collapsibles[i])
        st = statistics[collapsibles[i]] if collapsibles[i] in statistics.keys() else ["N/A"]*4
        n = nulls[collapsibles[i]] if collapsibles[i] in nulls.keys() else [0,0]
        collapsible.add_statistics(n, st, data, collapsibles[i], varType)
        collapsible.pack(fill='x')
    
    collapsibles_container.pack(fill="both", expand=True)
    return collapsibles_container  

def show_main_window(X):
    root = tk.Tk()
    root.title("Data Science - Proyecto 1")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[20, 10], font=('Arial', 14))
    
    categorical, continuous, discreet = identifyVariables(X)
    null_values = getNulls(X)
    numerics = continuous + discreet
    statistics = getStatistics(X, numerics)
    
    for tab_name in ["Categóricas", "Continuas", "Discretas"]:
        if tab_name == "Categóricas":
            tab_content = create_tab_content(notebook, categorical, null_values, statistics, X, "CAT")
        elif tab_name == "Continuas":
            tab_content = create_tab_content(notebook, continuous, null_values, statistics, X, "CONT")
        else:
            tab_content = create_tab_content(notebook, discreet, null_values, statistics, X, "DISC")
        notebook.add(tab_content, text=tab_name)

    notebook.pack(expand=True, fill="both")

    def update_tabs(event):
        total_width = notebook.winfo_width()
        num_tabs = len(notebook.tabs())
        tab_width = total_width // num_tabs
        style.configure("TNotebook.Tab", width=tab_width)

    root.bind("<Configure>", update_tabs)

    # Adding a button in the bottom right corner
    corner_button = ttk.Button(root, text="Gráfica de 2 variables.", command=lambda: open_selection_window(X))
    corner_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    root.mainloop()

def open_selection_window(X):
    columns = X.columns
    selection_window = tk.Toplevel()
    selection_window.title("Seleccionar variables")
    selection_window.geometry("300x400")

    listbox = tk.Listbox(selection_window, selectmode=tk.MULTIPLE)
    for col in columns:
        listbox.insert(tk.END, col)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def confirm_selection():
        selected_indices = listbox.curselection()
        if len(selected_indices) == 2:
            selected_items = [columns[i] for i in selected_indices]
            getPlotTwoVariables(X, selected_items[0], selected_items[1])
            selection_window.destroy()
        else:
            messagebox.showwarning("Error", "Debes seleccionar exactamente 2 variables.")

    confirm_button = ttk.Button(selection_window, text="Confirmar", command=confirm_selection)
    confirm_button.pack(pady=20)

def load_csv_file():
    temp_window = tk.Tk()
    temp_window.title("Cargar CSV")
    temp_window.geometry("300x100")

    def on_load():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = pd.read_csv(file_path)
            temp_window.destroy()
            show_main_window(data)

    load_button = ttk.Button(temp_window, text="Cargar CSV", command=on_load)
    load_button.pack(pady=20)

    temp_window.mainloop()

load_csv_file()
