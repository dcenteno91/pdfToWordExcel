print("Iniciando la aplicación...")

import tkinter as tk
from gui import setup_gui
from controllers.main_controller import MainController
import os
import sys

def main():
  root = tk.Tk() 
  
  # Icono de la aplicación
  if hasattr(sys, '_MEIPASS'):
    project_dir = sys._MEIPASS
  else:
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
  icon_path = os.path.join(project_dir, 'assets', 'app.ico')
  #print(f"Icon path: {icon_path}")
  root.iconbitmap(icon_path)
  app = setup_gui(root)
  controller = MainController(app)
  root.mainloop()

if __name__ == "__main__":  
  main()