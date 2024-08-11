import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
# Asegúrate de tener esta función en el archivo de análisis
from analysis_module import analyze_data


def load_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("CSV files", "*.csv"),
        ("Excel files", "*.xlsx"),
        ("All files", "*.*")
    ])

    if file_path:
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                messagebox.showerror(
                    "Invalid File", "Unsupported file format!")
                return

            messagebox.showinfo(
                "Success", f"File loaded successfully: {file_path}")
            # Habilita el botón de análisis
            analyze_button['state'] = tk.NORMAL
            # Almacena el DataFrame en un atributo del botón para usarlo en la función de análisis
            analyze_button.data = data
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading the file: {str(e)}")


def analyze_data_gui():
    if hasattr(analyze_button, 'data'):
        data = analyze_button.data
        analyze_data(data)  # Llama a la función de análisis de datos
    else:
        messagebox.showwarning(
            "No Data", "No file loaded. Please load a file first.")


# Crea la ventana principal
root = tk.Tk()
root.title("Herramienta para anális de datos")
root.geometry('800x400')

# Aplica un tema a los widgets
style = ttk.Style()
style.theme_use('xpnative')

# Crea un marco para los widgets con padding
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

# Crea una etiqueta y la añade al marco
label = ttk.Label(frame, text="Selecciona el archivo:")
label.pack(pady=10)

# Crea un botón para cargar archivos y lo añade al marco
load_button = ttk.Button(frame, text="Cargar archivo", command=load_file)
load_button.pack(pady=10)

# Crea un botón para realizar el análisis de datos
analyze_button = ttk.Button(
    frame, text="Analizar datos", command=analyze_data_gui, state=tk.DISABLED)
analyze_button.pack(pady=10)

# Inicia el loop de eventos de la ventana
root.mainloop()
