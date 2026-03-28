import tkinter as tk

class LoadingFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.loadingText = tk.Label(self, text= "Loading...")
        self.loadingText.pack(fill="Both", expand=True)

        self.pack(fill="both", expand=True)