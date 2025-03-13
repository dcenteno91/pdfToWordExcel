print("Iniciando la aplicación...")

import tkinter as tk
from gui import setup_gui
from controllers.main_controller import MainController
import tabula

def main():
  root = tk.Tk()
  app = setup_gui(root)
  controller = MainController(app)
  root.mainloop()

if __name__ == "__main__":  
  main()