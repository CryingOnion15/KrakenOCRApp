import tkinter as tk
from pathlib import Path
from Widgets.ScrollField import ScrollField
from tkinter import simpledialog
import re

class ModelCreationTab(tk.Frame):

    def __init__(self, master=None, **kwargs):
        # Call super init
        super().__init__(master, **kwargs)

        self.modelPath = Path("Models")
        self.modelNames = []

        #This should never happen.
        if not self.modelPath.exists():
            self.modelPath.mkdir(parents=True, exist_ok=False)
        
        self.SetupFrame()
        self.UpdateModelNames()

    def GetModelNames(self):
        return self.modelNames
    
    def GetModelTrainingFolder(self, modelName):
        return self.modelPath / modelName / "training"
    
    def GetModelOutFolder(self, modelName):
        return self.modelPath / modelName / "output"

    def UpdateModelNames(self):
        self.modelNames = []
        modelNames = [model.name for model in self.modelPath.iterdir() if model.is_dir()]
        self.modelNames = modelNames
        self.modelPathcrollField.setLabels(modelNames)    

    def SetupFrame(self):
        # Setup rows & columns of parent frame.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=8)

        # Create buttons
        self.addButton = tk.Button(self, text="+", font= ("Arial",18), width=4)
        self.addButton.grid(row=0, column=0, sticky= "nwse", padx= 10)
        self.addButton.bind("<Button-1>", self.addNewModel)

        self.removeButton = tk.Button(self, text="-", font= ("Arial",18), width=4)
        self.removeButton.grid(row=0, column=1, sticky= "nwse", padx= 10)
        self.removeButton.bind("<Button-1>", self.removeModel)

        # Add Scroll Field
        self.modelPathcrollField = ScrollField(self)
        self.modelPathcrollField.grid(row = 1, column=0, columnspan=3, padx= 10, pady= 10, sticky="nswe")

        # Pack the final frame.
        self.pack(fill="both")

    def addNewModel(self, event):
        result = simpledialog.askstring("New Model", "Enter New Model Name: ")

        if(result is not None and result not in self.modelNames):
            result = re.sub(r"\s+", "-", result)

            self.CreateModelData(result)
            self.UpdateModelNames()

    def CreateModelData(self, newModelName):
        newModelFolder = self.modelPath / newModelName
        newModelFolder.mkdir(parents="True", exist_ok=False)

        newModelTraining = newModelFolder / "training"
        newModelTraining.mkdir(parents="True", exist_ok=False)

        newModelOutput = newModelFolder / "output"
        newModelOutput.mkdir(parents="True", exist_ok=False)

    #TODO NEED ADD a SELECTION that will allow for deletion.
    def removeModel(self, event):
        pass

