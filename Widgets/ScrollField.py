import tkinter as tk


class ScrollField(tk.Canvas):

    def __init__(self, master=None, supportSelection=False, **kwargs):
        self.backgroundColor = (kwargs.pop('viewBG', "#282828"))
        self.labelBackgroundColor = kwargs.pop('labelBG', "#505050")
        self.selectedColor = kwargs.pop('selectedBG', "#497ECD")
        self.clickCallback = kwargs.pop('clickCallback', None)
        self.selected = -1
        self.supportSelection = supportSelection

        super().__init__(master, **kwargs)

        self.labelFrame = tk.Frame(self)
        self.labelFrame.config(bg=self.backgroundColor)
        self.labelFrame.pack(fill='both', expand=True)
        self.nameLabels = []

    def setLabels(self, names=[]):
        #destroy old name labels
        for label in self.nameLabels:
            label.destroy()

        self.nameLabels = []
        counter = 0
        for name in names:
            newLabel = tk.Label(self.labelFrame, text=name, font=('Arial', 18))
            newLabel.config(bg=self.labelBackgroundColor)
            newLabel.pack(fill='x', expand=False)
            newLabel.bind("<Button-1>", lambda e, i=counter: self.select(i))
            counter += 1
            self.nameLabels.append(newLabel)

        self.labelFrame.pack()

    def select(self, index):
        if self.supportSelection:
            if(self.selected != -1):
                self.nameLabels[self.selected].config(bg=self.labelBackgroundColor)

            if self.selected == index:
                self.selected = -1
            else:
                self.selected = index
                self.nameLabels[index].config(bg=self.selectedColor)
            
            if self.clickCallback:
                self.clickCallback(self.selected)

    def GetSelectedText(self):
        if self.supportSelection and not self.selected == -1:
            return self.nameLabels[self.selected].cget("text")
        return None

    def GetSelectedIndex(self):
        if self.supportSelection:
            return self.selected
        return None
            


