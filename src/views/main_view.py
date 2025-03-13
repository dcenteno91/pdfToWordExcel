import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from PIL import Image, ImageTk  # Importar las clases necesarias
from pdf2docx import Converter  # Importar la clase Converter
import tabula
import pandas as pd
from tkinter import messagebox
import sys

class MainView:
  def __init__(self, root):    
    self.root = root
    self.root.title("Pantalla Principal")
    self.root.geometry("720x400")  # Tamaño de la nueva ventana    
    self.root.config(bg="lightblue")  # Cambiar el color de fondo de la ventana
    self.root.resizable(False, False)  # Evitar que la ventana sea redimensionable

    # Crear un Label para mostrar el título de la aplicación
    title_label = tk.Label(root, text="Convertidor de PDF a Word y Excel", font=("Arial", 20), bg="lightblue", foreground="blue")
    title_label.pack(pady=10)  # Centrar el título y agregar espacio vertical
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  # Centrar el título en la parte superior de la ventana    
                        
    # Cargar la imagen desde el directorio del proyecto
    if hasattr(sys, '_MEIPASS'):
        project_dir = sys._MEIPASS
    else:
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
    image_path = os.path.join(project_dir, 'assets', 'img-app.png')
    # # Redimensionar la imagen usando Pillow
    try:
      image = Image.open(image_path)
      image = image.resize((300, 170), Image.LANCZOS)
      photo = ImageTk.PhotoImage(image)
      image_label = tk.Label(root, image=photo, bg="lightblue")
      image_label.image = photo
      image_label.pack(pady=10)
      # Centrar imagen en la ventana principal
      image_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
      
    except Exception as e:
      messagebox.showerror(f"Error al cargar la imagen", e)

    
    # Agregar botón para seleccionar archivo
    select_file_button = tk.Button(root, text="Seleccionar PDF para convertir a WORD", command=lambda: self.select_file(tipo="word"))
    select_file_button.pack(pady=20)  # Centrar el botón y agregar espacio vertical
    select_file_button.place(relx=0.5, rely=0.68, anchor=tk.CENTER)  # Centrar el botón en la parte inferior de la ventana

    # Agregar botón para seleccionar archivo
    select_file_button = tk.Button(root, text="Seleccionar PDF para convertir a EXCEL", command=lambda: self.select_file(tipo="excel"))
    select_file_button.pack(pady=20)  # Centrar el botón y agregar espacio vertical
    select_file_button.place(relx=0.5, rely=0.77, anchor=tk.CENTER)  # Centrar el botón en la parte inferior de la ventana

    footer_label = tk.Label(self.root, text=f"Desarrollado por: Daniel Centeno", bg="lightblue", foreground="#333")
    footer_label.pack(pady=10)
    footer_label.place(relx=0.5, rely=0.98, anchor=tk.CENTER)

  def select_file(self, tipo):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path: # Si se selecciona un archivo
      # Agregar texto para indicar que el archivo se está procesando
      processing_label = tk.Label(self.root, text="Procesando archivo...", bg="lightblue", foreground="black")
      processing_label.pack(pady=10)
      processing_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

      # Agregar spinner para indicar que el archivo se está procesando
      spinner = ttk.Progressbar(self.root, mode='indeterminate', length=200)
      spinner.pack(pady=10)
      spinner.place(relx=0.5, rely=0.90, anchor=tk.CENTER)
      spinner.start()

      # Actualizar la interfaz gráfica
      self.root.update_idletasks()

      # Convertir el archivo PDF a Word o Excel según el tipo seleccionado
      success_label = None
      if tipo == "word":
        self.convert_to_word(file_path)

        # Mostrar un mensaje de éxito
        docx_path = file_path.replace('.pdf', '.docx')        
        success_label = tk.Label(self.root, text=f"Archivo convertido a WORD con éxito {docx_path}", bg="lightblue", foreground="blue")
        success_label.pack(pady=10)
        success_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
      else:
        self.convert_to_excel(file_path)
        
        # Mostrar un mensaje de éxito
        xslx_path = file_path.replace('.pdf', '.xlsx')
        success_label = tk.Label(self.root, text=f"Archivo convertido a EXCEL con éxito en {xslx_path}", bg="lightblue", foreground="green")
        success_label.pack(pady=10)
        success_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
      
      # Detener el spinner y mensaje de procesamiento después de 1 segundo
      self.root.after(1000, lambda: self.stopSpinner(spinner, processing_label))                  

  def stopSpinner(self, spinner, processing_label):
    spinner.stop()
    spinner.destroy()
    processing_label.destroy()

  def convert_to_word(self, pdf_path):
    # Definir la ruta de salida para el archivo Word
    docx_path = pdf_path.replace('.pdf', '.docx')
    
    # Crear un convertidor PDF a Word
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

  def convert_to_excel(self, pdf_path):
    # Definir la ruta de salida para el archivo Excel
    excel_path = pdf_path.replace('.pdf', '.xlsx')
    
    # Convertir el archivo PDF a Excel usando tabula-py
    try:
      # Leer todas las tablas del PDF
      dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

      # Crear un objeto ExcelWriter para guardar múltiples DataFrames en un solo archivo Excel
      with pd.ExcelWriter(excel_path) as writer:
        for i, df in enumerate(dfs):
          df.to_excel(writer, sheet_name=f'Hoja{i+1}', index=False)

    except Exception as e:
      messagebox.showerror(f"Error al convertir el archivo a Excel", e)