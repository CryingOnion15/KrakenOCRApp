import tkinter as tk;
from tkinter import ttk
from Pages.ModelAddTrainingData import ModelAddTrainingDataTab
from Pages.ModelCreation import ModelCreationTab

root = tk.Tk()
root.title("Recipe Reader")
root.geometry("800x500")

mainWindow = ttk.Notebook(root)
mainWindow.pack(fill='both', expand=True) 

modelCreationTab = ModelCreationTab(mainWindow, name="modelCreation")
trainingTab = ModelAddTrainingDataTab(mainWindow, models=modelCreationTab.GetModelNames(), name="modelTraining")

# Add Tabs
mainWindow.add(modelCreationTab, text="Model Add/Select")
mainWindow.add(trainingTab, text="Training")

mainWindow.select(modelCreationTab)

root.mainloop()
