import tkinter as tk
from Widgets.ScrollField import ScrollField
from tkinter import filedialog
from pathlib import Path

class ModelTrainingTab(tk.Frame):

    def __init__(self, master=None, **kwargs):
        # Call super init
        super().__init__(master, **kwargs)

        # Create UI
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        self.uploadBttn = tk.Button(self, text="Upload Files", font=('Arial', 18))
        self.uploadBttn.grid(row=0, column=0, sticky="we")
        self.uploadBttn.bind("<Button-1>", self.uploadFiles)

        self.fileNameDisplay = ScrollField(self)
        self.fileNameDisplay.grid(row=1, column=0, sticky="nswe")

        self.pack(fill='both', expand=True)

    def uploadFiles(self, event):
        #Reset the data.
        filePaths = []
        fileNames = []

        #Get all selected file paths.
        filePaths = filedialog.askopenfilenames(initialdir="./", title="Select Files to Upload", filetypes=(("PNG","*.png"),))

        if filePaths:
            for file in filePaths:
                fileNames.append(Path(file).name)
            
            self.fileNameDisplay.setLabels(fileNames)