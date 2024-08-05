import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas
from tkinter import filedialog, messagebox  # Importa filedialog y messagebox para diálogos de archivos y mensajes
from tkinter import ttk  # Importa ttk para widgets temáticos
import pandas as pd  # Importa pandas para manipulación de datos

def load_file():
    """
    Abre un cuadro de diálogo para seleccionar un archivo y carga el contenido del archivo seleccionado.
    Soporta archivos CSV y Excel. Muestra mensajes de éxito o error según corresponda.
    """
    # Abre un cuadro de diálogo para seleccionar un archivo
    file_path = filedialog.askopenfilename(filetypes=[
        ("CSV files", "*.csv"),  # Filtro para archivos CSV
        ("Excel files", "*.xlsx"),  # Filtro para archivos Excel
        ("All files", "*.*")  # Filtro para todos los archivos
    ])
    
    if file_path:  # Si se selecciona un archivo
        try:
            # Carga el archivo según su extensión
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)  # Carga archivo CSV
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)  # Carga archivo Excel
            else:
                # Muestra un mensaje de error si el formato del archivo no es soportado
                messagebox.showerror("Invalid File", "Unsupported file format!")
                return
            
            # Muestra un mensaje de éxito si el archivo se carga correctamente
            messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
            # Imprime las primeras filas del archivo cargado
            print(data.head())
        except Exception as e:
            # Muestra un mensaje de error si ocurre un problema al cargar el archivo
            messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")

# Crea la ventana principal
root = tk.Tk()
root.title("File Loader")  # Título de la ventana

# Establece el tamaño de la ventana
root.geometry('800x400')

# Aplica un tema a los widgets
style = ttk.Style()
style.theme_use('xpnative')

# Crea un marco para los widgets con padding
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)  # Expande el marco para llenar la ventana

# Crea una etiqueta y la añade al marco
label = ttk.Label(frame, text="Select a file to load:")
label.pack(pady=10)  # Añade padding vertical

# Crea un botón para cargar archivos y lo añade al marco
load_button = ttk.Button(frame, text="Load File", command=load_file)
load_button.pack(pady=20)  # Añade padding vertical

# Inicia el loop de eventos de la ventana
root.mainloop()