import tkinter as tk
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
    def __init__(self, master):
        self.master = master
        self.master.title("Age Of Empires")
        self.master.attributes('-fullscreen', True)
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
        print("Le jeu commence...")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()

    # Create an instance of the FenetreJeu class
    fenetre = FenetreJeu(root)

    # Start the main Tkinter loop
    root.mainloop()

