import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from utils import *

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._visible = False  # Start as collapsed
        self._title = title

        # Create the header with a toggle button
        self.header = ttk.Frame(self)
        self.toggle_button = ttk.Button(self.header, text=self._title, command=self.toggle)
        self.toggle_button.pack(fill='x')
        self.header.pack(fill='x')

        # Create the content area
        self.content = ttk.Frame(self)
        self.content.pack_forget()  # Start hidden
        
        self.content_grid = ttk.Frame(self.content)
        self.content_grid.pack(fill="both", expand=True)
        
        self.stats_frame = ttk.Frame(self.content_grid)
        self.stats_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.button_frame = ttk.Frame(self.content_grid)
        self.button_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Configure grid weights to ensure proper resizing
        self.content_grid.grid_columnconfigure(0, weight=1)
        self.content_grid.grid_columnconfigure(1, weight=2)  # Adjust the weight for the button section
        self.content_grid.grid_rowconfigure(0, weight=1)

        self.graph_type = tk.StringVar(value="Gráfico de Barras")
        self.data = None  # To store data for plotting
        self.variable = None  # To store the variable name for plotting

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

        # Add labels for statistics
        labels = ["Media:", "Mediana:", "Moda:", "Desviación estándar:", "Valores nulos"]
        values = [f"{st[0]}",
                  f"{st[1]}",
                  f"{st[2]}",
                  f"{st[3]}\n",
                  f"{n[0]} ({n[1]*100:.2f}% del total)."]
        for row, (label, value) in enumerate(zip(labels, values)):
            ttk.Label(self.stats_frame, text=label).grid(row=row, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(self.stats_frame, text=value).grid(row=row, column=1, sticky='w', padx=5, pady=2)

        # Add a menu to choose the graph type
        self.graph_menu = ttk.Combobox(self.button_frame, values=getPlotSingleVariableTypes(varType), textvariable=self.graph_type, state='readonly')
        self.graph_menu.pack(pady=5)
        
        self.graph_button = ttk.Button(self.button_frame, text="Generar gráfico", command=self.generate_graph)
        self.graph_button.pack(pady=10)
        
    def generate_graph(self):
        # Get the selected graph type
        graph_type = self.graph_type.get()

        # Define font size
        font_size = 8  # Adjust this value to your preference

        # Get the figure and axes from the getPlotByType function
        if self.data is not None and self.variable is not None:
            fig, ax = getPlotByType(graph_type, self.data, self.variable, font_size)
        else:
            fig, ax = plt.subplots(figsize=(4,3))
            ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', fontsize=font_size)
            ax.set_title('Error', fontsize=font_size)
        
        # Adjust the font size for axis labels and ticks if needed
        ax.title.set_fontsize(font_size)
        ax.xaxis.label.set_fontsize(font_size)
        ax.yaxis.label.set_fontsize(font_size)
        ax.tick_params(axis='both', which='major', labelsize=font_size)
        
        # Clear the existing widgets in the button frame and add the new graph
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Create a FigureCanvasTkAgg widget to display the graph
        canvas = FigureCanvasTkAgg(fig, master=self.button_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

def create_tab_content(parent, collapsibles, nulls, statistics, data, varType):
    # Create a frame to contain the collapsibles and add a scrollbar to it
    collapsibles_container = ttk.Frame(parent)
    
    # Create a canvas and vertical scrollbar
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
    return collapsibles_container  # Return the container instead of canvas directly

def show_main_window(X):
    # Create the main application window
    root = tk.Tk()
    root.title("Data Science - Proyecto 1")
    root.geometry("800x600")

    # Create a notebook (tabs container)
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

    # Pack the notebook (add it to the main window)
    notebook.pack(expand=True, fill="both")

    def update_tabs(event):
        total_width = notebook.winfo_width()
        num_tabs = len(notebook.tabs())
        tab_width = total_width // num_tabs
        style.configure("TNotebook.Tab", width=tab_width)

    root.bind("<Configure>", update_tabs)
    root.mainloop()

def load_csv_file():
    # Create a temporary window to load the CSV file
    temp_window = tk.Tk()
    temp_window.title("Cargar CSV")
    temp_window.geometry("300x100")

    def on_load():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            # You can process the file_path if needed
            data = pd.read_csv(file_path)
            temp_window.destroy()
            show_main_window(data)

    load_button = ttk.Button(temp_window, text="Cargar CSV", command=on_load)
    load_button.pack(pady=20)

    temp_window.mainloop()

# Start the application with the CSV file load window
load_csv_file()
