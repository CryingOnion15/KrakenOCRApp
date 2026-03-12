import tkinter as tk;
from tkinter import ttk
from Pages.ModelTraining import ModelTrainingTab
from Pages.ModelCreation import ModelCreationTab

root = tk.Tk()
root.title("Recipe Reader")
root.geometry("800x500")

mainWindow = ttk.Notebook(root)
mainWindow.pack(fill='both', expand=True) 

modelCreationTab = ModelCreationTab(mainWindow, name="modelCreation")
trainingTab = ModelTrainingTab(mainWindow, name="modelTraining")

# Add Tabs
mainWindow.add(modelCreationTab, text="Model Add/Select")
mainWindow.add(trainingTab, text="Training")

mainWindow.select(modelCreationTab)

root.mainloop()


