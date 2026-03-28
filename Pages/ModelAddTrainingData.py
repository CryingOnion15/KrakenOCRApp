import tkinter as tk
from tkinter import ttk
import threading
import pymupdf as PDF
from PIL import Image
from Widgets.ScrollField import ScrollField
from Widgets.Loading.ProgressBarLoadingFrame import ProgressBarLoadingFrame
from tkinter import filedialog
from pathlib import Path
from kraken import binarization
from kraken import pageseg
from kraken.serialization import serialize
from io import BytesIO

class ModelAddTrainingDataTab(tk.Frame):

    def __init__(self, master=None, models=[], **kwargs):
        # Call super init
        super().__init__(master, **kwargs)

        self.modelNames = models

        # Create UI
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.showAddDataFrame()

        self.pack(fill='both', expand=True)

        ## Variables
        self.filePaths = []
        self.fileNames = []
        self.fileUploadMax = 0
        self.currentFile = 0

    def showLoadingFrame(self, maximum, instruction):
        self.loadingFrame = ProgressBarLoadingFrame(self, loadText="Binarizing and uploading all training images.")
        self.loadingFrame.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="nswe", padx= 10, pady=10)
        self.loadingFrame.intializeProgress(maximum, instruction)
        

    def showAddDataFrame(self):
        #Column 1
        self.modelSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1")
        self.modelSelection.grid(row=0, column=0, rowspan=3, sticky="nswe", pady=10, padx=3)
        self.modelSelection.setLabels(self.modelNames)

        #Column 2
        self.uploadBttn = tk.Button(self, text="Upload Files", font=('Arial', 18))
        self.uploadBttn.grid(row=0, column=1, columnspan=2, sticky="we")
        self.uploadBttn.bind("<Button-1>", self.uploadFiles)

        self.fileNameDisplay = ScrollField(self)
        self.fileNameDisplay.grid(row=1, column=1, columnspan=2, sticky="nswe")

        #DPI and save button.
        self.dpiFrame = tk.Frame(self)
        self.dpiLabel = tk.Label(self.dpiFrame, text="DPI:", font=('Arial', 12))
        self.dpiLabel.pack(side="left")
        self.dpiValue = ttk.Spinbox(self.dpiFrame, from_=30, to=600)
        self.dpiValue.pack(side="left", padx=10)
        self.dpiFrame.grid(row=2, column=1, sticky="news", padx=10)

        self.saveDataBttn = tk.Button(self, text="Save Training Data", font=('Arial', 12))
        self.saveDataBttn.grid(row=2, column=2, sticky="e" , padx=10)
        self.saveDataBttn.bind("<Button-1>", self.saveData)


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

    def resetFrameData(self):
        self.filePaths = []
        self.fileNames = []
        self.fileUploadMax = 0
        self.currentFile = 0

    def getFileCount(self):
        count = 0

        for index in range(len(self.filePaths)):
            filePath = self.filePaths[index]
            fileExt = Path(filePath).suffix
            
            if(fileExt == ".png"):
                count += 1
            elif(fileExt == ".pdf"):
                doc = PDF.open(filePath)
                count += doc.page_count
                doc.close()

        return count

    def saveData(self, event):
        if self.modelSelection.GetSelectedText() is None:
            return
        
        self.fileUploadMax = self.getFileCount()
        self.currentFile = 0
        self.showLoadingFrame(self.fileUploadMax, f"Processing file {self.currentFile} of {self.fileUploadMax}")

        # Start a background process of uploading the files.
        processThread = threading.Thread(target=self.processFiles)
        processThread.daemon = True
        processThread.start()

    def processFiles(self):
        for index in range(len(self.filePaths)):
            filePath = self.filePaths[index]
            fileExt = Path(filePath).suffix
            fileName = self.fileNames[index]

            if(fileExt == ".png"):
                #Binarize the image and save it to the training folder.
                png = Image.open(filePath)
                self.loadingFrame.updateStep(0, f"Binarizing: {fileName}")
                binImg = binarization.nlbin(png)
                self.loadingFrame.updateStep(.25, f"Binarized: {fileName}")
                binImg.save("./Models/" + self.modelSelection.GetSelectedText() + "/training/" + fileName)
                

                # Segment Binary Image.
                self.loadingFrame.updateStep(.25, f"Creating Segmentation of: {fileName}")
                segData = pageseg.segment(binImg)

                # Serialize and Save Segmentation.
                self.loadingFrame.updateStep(.5, f"Serialzing Segmentation of: {fileName}")
                with open(f"./Models/{self.modelSelection.GetSelectedText()}/output/{fileName}_seg.xml", "w", encoding="utf-8") as file:
                    file.write(serialize(segData))

                self.loadingFrame.updateStep(0, f"Training Data created for: {fileName}")

                self.currentFile += 1
                self.loadingFrame.updateInstructionText(f"Processing file {self.currentFile + 1} of {self.fileUploadMax}")

            elif(fileExt == ".pdf"):
                #Open PDF and turn each page into png.
                doc = PDF.open(filePath)
                pageNumber = 0
                for page in doc:
                    # Convert to PNG
                    self.loadingFrame.updateStep(0, f"Converting page {pageNumber + 1} of {fileName} into PNG")
                    png_bytes = page.get_pixmap(dpi=int(self.dpiValue.get())).tobytes("png")
                    img = Image.open(BytesIO(png_bytes))

                    # Binarize the image and save it to the training folder.
                    trainingFolder = "./Models/" + self.modelSelection.GetSelectedText() + "/training/"
                    imgName = fileName + "_" + str(pageNumber) + ".png"

                    self.loadingFrame.updateStep(0, f"Binarizing page {pageNumber + 1}")
                    binImg = binarization.nlbin(img)
                    self.loadingFrame.updateStep(.25, f"Binarized page {pageNumber + 1}")
                    binImg.save(trainingFolder + imgName)

                    # Segment Binary Image.
                    self.loadingFrame.updateStep(.25, f"Creating Segmentation of page: {pageNumber + 1}")
                    segData = pageseg.segment(binImg)

                    # Serialize and Save Segmentation.
                    self.loadingFrame.updateStep(.5, f"Serialzing Segmentation of page: {pageNumber + 1}")
                    with open(f"./Models/{self.modelSelection.GetSelectedText()}/output/{fileName}_{pageNumber + 1}_seg.xml", "w", encoding="utf-8") as file:
                        file.write(serialize(segData))
                    
                    self.loadingFrame.updateStep(0, f"Training Data created for: {fileName} Page {pageNumber + 1}")

                    pageNumber += 1
                    self.currentFile += 1
                    self.loadingFrame.updateInstructionText(f"Processing file {self.currentFile + 1} of {self.fileUploadMax}")
                doc.close()

        self.after(0, self.resetFrameData)
        self.after(50, self.showAddDataFrame)

    def createTrainingDataFromImg(self, img, fileName):
        self.loadingFrame.updateStep(0, f"Binarizing: {fileName}")
        binImg = binarization.nlbin(img)
        self.loadingFrame.updateStep(.25, f"Binarized: {fileName}")
        binImg.save(f"./Models/{self.modelSelection.GetSelectedText()}/training/{fileName}")
        

        # Segment Binary Image.
        self.loadingFrame.updateStep(.25, f"Creating Segmentation of: {fileName}")
        segData = pageseg.segment(binImg)

        # Serialize and Save Segmentation.
        self.loadingFrame.updateStep(.5, f"Serialzing Segmentation of: {fileName}")
        with open(f"./Models/{self.modelSelection.GetSelectedText()}/output/{fileName}_seg.xml", "w", encoding="utf-8") as file:
            file.write(serialize(segData))

        self.loadingFrame.updateStep(0, f"Training Data created for: {fileName}")

        self.currentFile += 1
        self.loadingFrame.updateInstructionText(f"Processing file {self.currentFile + 1} of {self.fileUploadMax}")