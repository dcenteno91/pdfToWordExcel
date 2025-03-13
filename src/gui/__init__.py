# This file is intentionally left blank.
import tkinter as tk
import views.login_view as LoginView
import views.main_view as MainView

def setup_gui(root):
    MainView.MainView(root)
    #LoginView.LoginView(root)
    return root