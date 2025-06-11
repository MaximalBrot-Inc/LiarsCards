import customtkinter as ctk
import lib_code as lc
import threading
import subprocess
import sys
import os
from PIL import Image
import time


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("themes/orange.json")      
        self._set_appearance_mode("dark")             
        self.title("Liars Cards Launcher")
        self.geometry("800x600")

        self.launcher = lc.LauncherLib()

    def set_background(self):
        try:
            self.bg_image = ctk.CTkImage(
                light_image=Image.open("launcher_bg.png"),
                dark_image=Image.open("launcher_bg.png"),
                size=(self.winfo_width(), self.winfo_height())
            )
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print(f"Error loading background image: {str(e)}")

    def main_plot(self):
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.label = ctk.CTkLabel(
            self,
            text="Welcome to Liars Cards Launcher",
            font=("Arial", 20),
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.version_label = ctk.CTkLabel(
            self,
            text=f"Version: {self.launcher.get_version()}",
        )
        self.version_label.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
        )
        self.status_label.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    def button_init(self):
        # Direkt auf dem Hauptfenster platzierte Buttons
        self.button_start = ctk.CTkButton(
            self, 
            text="Start Game", 
            command=self.start_game,
            corner_radius=0,
            width=200,    # Breite in Pixel
            height=60     # Höhe in Pixel
        )
        self.button_start.grid(row=2, column=1, padx=20, pady=20)

        self.button_update = ctk.CTkButton(
            self, 
            text="Check for Updates", 
            command=self.check_for_updates,
            corner_radius=0,
            width=200,
            height=60
        )
        self.button_update.grid(row=2, column=0, padx=20, pady=20)

        self.button_quit = ctk.CTkButton(
            self, 
            text="Quit", 
            command=self.quit,
            corner_radius=0,
            width=200,
            height=60
        )
        self.button_quit.grid(row=2, column=2, padx=20, pady=20)

    def check_for_updates(self):
        self.status_label.configure(text="Checking for updates...")
       


    def start_game(self):
        self.status_label.configure(text="Starting the game...")

        def launch_task():
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                client_main = os.path.join(base_dir, "..", "client", "main.py")
                client_main = os.path.abspath(client_main)
                subprocess.Popen([sys.executable, client_main])
                self.status_label.configure(text="Game launched successfully!")
                time.sleep(3)
                self.quit()
            except Exception as e:
                self.status_label.configure(text=f"Error launching game: {str(e)}")

        threading.Thread(target=launch_task).start()

    def build(self):
        self.set_background()
        self.main_plot()
        self.button_init()
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if self.bg_image and (event.width > 1 and event.height > 1):
            self.bg_image.configure(size=(event.width, event.height))


