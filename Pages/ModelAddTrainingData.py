import tkinter as tk
import pymupdf as PDF
from PIL import Image
from Widgets.ScrollField import ScrollField
from tkinter import filedialog
from pathlib import Path
from kraken import binarization
from io import BytesIO

class ModelAddTrainingDataTab(tk.Frame):

    def __init__(self, master=None, models=[], **kwargs):
        # Call super init
        super().__init__(master, **kwargs)

        self.modelNames = models

        # Create UI
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        #Column 1
        self.modelSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1")
        self.modelSelection.grid(row=0, column=0, rowspan=3, sticky="nswe", pady=10, padx=3)
        self.modelSelection.setLabels(models)

        #Column 2
        self.uploadBttn = tk.Button(self, text="Upload Files", font=('Arial', 18))
        self.uploadBttn.grid(row=0, column=1, sticky="we")
        self.uploadBttn.bind("<Button-1>", self.uploadFiles)

        self.fileNameDisplay = ScrollField(self)
        self.fileNameDisplay.grid(row=1, column=1, sticky="nswe")

        self.saveDataBttn = tk.Button(self, text="Save Training Data", font=('Arial', 12))
        self.saveDataBttn.grid(row=2, column=1, sticky="e" , padx=10)
        self.saveDataBttn.bind("<Button-1>", self.saveData)

        self.pack(fill='both', expand=True)

        ## Variables
        self.filePaths = []
        self.fileNames = []

    def uploadFiles(self, event):
        #Reset the data.
        self.filePaths = []
        self.fileNames = []

        #Get all selected file paths.
        self.filePaths = filedialog.askopenfilenames(initialdir="./", title="Select PNGs or PDFs to Upload", filetypes=(("PNG","*.png"),("PDF","*.pdf")))

        if self.filePaths:
            for file in self.filePaths:
                self.fileNames.append(Path(file).stem)
            
            self.fileNameDisplay.setLabels(self.fileNames)

    def clearFiles(self):
        self.filePaths = []
        self.fileNames = []
        self.fileNameDisplay.setLabels([])

    def saveData(self, event):
        if self.modelSelection.GetSelectedText() is not None:
            for index in range(len(self.filePaths)):
                filePath = self.filePaths[index]
                fileExt = Path(filePath).suffix
                fileName = self.fileNames[index]

                if(fileExt == ".png"):
                    #Binarize the image and save it to the training folder.
                    png = Image.open(filePath)
                    binImg = binarization.nlbin(png)
                    binImg.save(self.modelSelection.GetSelectedText() + "/training/" + fileName)
                if(fileExt == ".pdf"):
                    #Open PDF and turn each page into png.
                    doc = PDF.open(filePath)
                    page = 0
                    for page in doc:
                        # Convert to PNG
                        png_bytes = page.get_pixmap().tobytes("png")
                        img = Image.open(BytesIO(png_bytes))

                        # Binarize the image and save it to the training folder.
                        binImg = binarization.nlbin(img)
                        print(fileName)
                        print(self.modelSelection.GetSelectedText() + "/training/" + fileName + "_" + page)
                        binImg.save(self.modelSelection.GetSelectedText() + "/training/" + fileName + "_" + page)
                        page += 1
                        print("Saved page " + str(page) + " of " + fileName)
                    doc.close()
            print("Data Saved")