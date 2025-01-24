"je propose les modifications suivante pour régler le problème de l'apparition de la fenêtre save comme fenêtre principal"
"c'est à intégrer au code initial de @yahya_amadou_diallou"

class Selectors:
    def __init__(self, name, parent):
        self.top = tk.Toplevel(parent)
        self.top.title(name)
        self.folder_path = ""
        self.file_path = ""

        self.select_button = tk.Button(self.top, text=f"{name}", command=self.select)
        self.select_button.pack(pady=20)

        self.close_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.close_button.pack(pady=20)

        # Center the sub-window on the screen
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

class FolderSelector(Selectors):
    def __init__(self, parent):
        super().__init__("Select folder", parent)

    def select(self):
        self.folder_path = filedialog.askdirectory(parent=self.top)
        if self.folder_path:
            print(f"Folder selected: {self.folder_path}")
            self.top.destroy()

class FileSelector(Selectors):
    def __init__(self, parent):
        super().__init__("Select File", parent)

    def select(self):
        self.file_path = filedialog.askopenfilename(parent=self.top)
        if self.file_path:
            print(f"File selected: {self.file_path}")
            self.top.destroy()
