import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd


def load_file():
    file_path = filedialog.askopenfilename(filetypes=[(
        "CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")])
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
            # Data.head del archivo
            print(data.head())
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading the file: {str(e)}")


# Crea la ventana
root = tk.Tk()
root.title("File Loader")

# Set the size of the window
root.geometry('800x400')

# Theme
style = ttk.Style()
style.theme_use('xpnative')

# Frame para widgets
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

# Label
label = ttk.Label(frame, text="Select a file to load:")
label.pack(pady=10)

# Creación de botón para cargar
load_button = ttk.Button(frame, text="Load File", command=load_file)
load_button.pack(pady=20)

# Loop de evento
root.mainloop()
