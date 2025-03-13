import tkinter as tk
from tkinter import filedialog
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
    self.root.geometry("720x360")  # Tamaño de la nueva ventana    
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
    
    image_path = os.path.join(project_dir, 'assets', 'img-app.jpg')

    # # Redimensionar la imagen usando Pillow
    try:
      image = Image.open(image_path)
      image = image.resize((300, 170), Image.LANCZOS)
      photo = ImageTk.PhotoImage(image)
      image_label = tk.Label(root, image=photo, bg="lightblue")
      image_label.image = photo
      image_label.pack(pady=10)
      # Centrar imagen en la ventana principal
      image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
      
    except Exception as e:
      print(f"Error al cargar la imagen: {e}")

    
    # Agregar botón para seleccionar archivo
    select_file_button = tk.Button(root, text="Seleccionar PDF para convertir a WORD", command=lambda: self.select_file(tipo="word"))
    select_file_button.pack(pady=20)  # Centrar el botón y agregar espacio vertical
    select_file_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # Centrar el botón en la parte inferior de la ventana

    # Agregar botón para seleccionar archivo
    select_file_button = tk.Button(root, text="Seleccionar PDF para convertir a EXCEL", command=lambda: self.select_file(tipo="excel"))
    select_file_button.pack(pady=20)  # Centrar el botón y agregar espacio vertical
    select_file_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Centrar el botón en la parte inferior de la ventana

    footer_label = tk.Label(self.root, text=f"Desarrollado por: Daniel Centeno", bg="lightblue", foreground="red")
    footer_label.pack(pady=10)
    footer_label.place(relx=0.5, rely=0.97, anchor=tk.CENTER)

    # def resource_path(relative_path):
    #   try:
    #     if hasattr(sys, '_MEIPASS'):
    #       base_path = sys._MEIPASS
    #     else:
    #       base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #   except Exception:
    #     base_path = os.path.abspath(".")
      
    #   return os.path.join(base_path, relative_path)

  def select_file(self, tipo):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path: 
      # Crear un nuevo Label para mostrar la ruta del archivo seleccionado
      msg = f"Archivo seleccionado: {file_path}"
      messagebox.showinfo("Éxito", msg)      

      # Convertir el archivo PDF a Word o Excel según el tipo seleccionado
      if tipo == "word":
        self.convert_to_word(file_path)
      else:
        self.convert_to_excel(file_path)

  def convert_to_word(self, pdf_path):
    # Definir la ruta de salida para el archivo Word
    docx_path = pdf_path.replace('.pdf', '.docx')
    
    # Crear un convertidor PDF a Word
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()
    
    # Mostrar un mensaje de éxito        
    success_label = tk.Label(self.root, text=f"Archivo convertido Word en: {docx_path}", bg="lightblue", foreground="blue")
    success_label.pack(pady=10)
    success_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

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

      # Mostrar un mensaje de éxito
      success_label = tk.Label(self.root, text=f"Archivo convertido a Excel en: {excel_path}", bg="lightblue", foreground="blue")
      success_label.pack(pady=10)
      success_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    except Exception as e:
      print(f"Error al convertir el archivo a Excel: {e}")