import tkinter as tk


class ScrollField(tk.Canvas):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.labelFrame = tk.Frame(self)
        self.labelFrame.config(bg="#282828")
        self.labelFrame.pack(fill='both', expand=True)
        self.nameLabels = []

    def setLabels(self, names=[]):

        #destroy old name labels
        for label in self.nameLabels:
            label.destroy()

        self.nameLabels = []
        for name in names:
            newLabel = tk.Label(self.labelFrame, text=name, font=('Arial', 18))
            newLabel.config(bg='#505050')
            newLabel.pack(fill='x', expand=False)
            self.nameLabels.append(newLabel)

        self.labelFrame.pack()
            


