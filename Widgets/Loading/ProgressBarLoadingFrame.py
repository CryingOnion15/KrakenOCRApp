import tkinter as tk
from tkinter import ttk

class ProgressBarLoadingFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        self.loadingText = kwargs.pop("loadText", "Loading...")

        super().__init__(master, **kwargs)
        #Setup rows of the frame.
        self.rowconfigure(0, weight=1) #Generic Loading Text
        self.rowconfigure(1, weight=1) #Progress Text
        self.rowconfigure(2, weight=1) #Progress Bar
        self.rowconfigure(3, weight=1) #Current Step Messages
        self.columnconfigure(0, weight=1)

        #Row 1
        self.loadingText = tk.Label(self, text=self.loadingText, font=('Arial', 18))
        self.loadingText.grid(row=0, column=0)

        self.progressLabel = tk.Label(self, font=('Arial', 18), text="")
        self.currentValue = tk.DoubleVar(self, value=0)
        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate", variable=self.currentValue)
        self.progressLabel.grid(row= 1, column= 0, sticky= "we")
        self.progressBar.grid(row= 2, column= 0, sticky= "we")

        self.currentStepLabel = tk.Label(self, font=('Arial', 12), text="")
        self.currentStepLabel.grid(row=3, column=0, sticky="we")

    def intializeProgress(self, maximumValue, instructionText=""):
        self.progressLabel.configure(text=instructionText)
        self.progressBar.configure(maximum=maximumValue)

    def updateStep(self, increment, stepText):
        self.currentStepLabel.configure(text=stepText)

        currentValue = self.currentValue.get()
        self.currentValue.set(currentValue + increment)

    def updateInstructionText(self, newText):
        self.progressLabel.configure(text=newText)
