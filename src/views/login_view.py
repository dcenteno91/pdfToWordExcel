import tkinter as tk
from tkinter import messagebox
from views.main_view import MainView

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi App GUI - Login")
        self.root.geometry("400x300")  # Establece el tamaño de la ventana
        
        # Etiqueta y campo de entrada para el nombre de usuario
        username_label = tk.Label(root, text="Nombre de usuario:")
        username_label.pack(pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        # Etiqueta y campo de entrada para la contraseña
        password_label = tk.Label(root, text="Contraseña:")
        password_label.pack(pady=10)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        login_button = tk.Button(root, text="Iniciar sesión")
        login_button.pack(pady=20)

        # Evento de clic en el botón de inicio de sesión 
        login_button.bind("<Button-1>", self.login)

    def login(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "" and password == "":  # Credenciales de ejemplo
            msg = f"Bienvenido, {username}!"
            messagebox.showinfo("Inicio de sesión exitoso", msg)
            self.open_main_window()
        else:
            messagebox.showwarning("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")
    
    def open_main_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()        
        MainView(self.root)