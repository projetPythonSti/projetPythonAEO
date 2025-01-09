import tkinter as tk
from tkinter import filedialog
import pygame 
from pygame import mixer
from PIL import Image, ImageTk

class GUIView:
    
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.icon = pygame.image.load("assets/logo.png")
        self.running = False
        
    
    def main(self):
        pygame.init()
        mixer.init()

        pygame.display.set_caption("Age of Empires")
        pygame.display.set_icon(self.icon)

        self.running = True
        
        


class game:
    
    def __init__(self):
        pass

class FenetreJeu:
    def __init__(self, luncher):
        self.luncher = luncher
        self.master = luncher.root
        self.master.title("Age Of Empires")
        self.master.geometry("800x600")
        self.master.resizable(False, False)  # Prevent resizing
        # Set the window icon
        self.master.iconbitmap('./assets/images/icon.ico') 
        self.background_image = ImageTk.PhotoImage(Image.open("./assets/images/sparta.jpeg"))
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Get the width and height of the window
        window_width = self.master.winfo_screenwidth()
        window_height = self.master.winfo_screenheight()

        # Calculate the positions to center the buttons
        button_width = 100
        button_height = 50
        x_position_jouer = (window_width // 2) - button_width - 10
        x_position_quitter = (window_width // 2) + 10
        y_position = (window_height // 2) - (button_height // 2)

        # Button "Jouer"
        self.bouton_jouer = tk.Button(self.master, text="Jouer", command=self.play)
        self.bouton_jouer.place(x=x_position_jouer, y=y_position, width=button_width, height=button_height)

        # Button "Quitter"
        self.bouton_quitter = tk.Button(self.master, text="Quitter", command=self.master.quit)
        self.bouton_quitter.place(x=x_position_quitter, y=y_position, width=button_width, height=button_height)

    def play(self):
        self.luncher.main()
        
class Selectors:
    def __init__(self, name, master=None):
        self.master = master if master else tk.Tk()
        self.folder_path = ""
        self.select_folder_button = tk.Button(self.master, text=name, command=self.select)
        self.select_folder_button.pack(pady=20)
        # Center the window on the screen
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

class FolderSelector(Selectors):
    def __init__(self, master=None):
        super().__init__("Select folder")
    
    def select(self):
        self.folder_path = filedialog.askdirectory()

class FileSelector(Selectors):
    def __init__(self, master=None):
        super().__init__("Select File")

    def select(self):
        self.file_path = filedialog.askopenfilename()

if __name__ == "__main__":
    # Create the main window
    # root = tk.Tk()

    # Create an instance of the FenetreJeu class
    # fenetre = FenetreJeu(root)
    file_selector = FileSelector()
    file_selector.master.mainloop()
    
    # Start the main Tkinter loop
    # root.mainloop()

