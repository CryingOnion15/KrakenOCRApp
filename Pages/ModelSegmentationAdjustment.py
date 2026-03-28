import tkinter as tk
from Widgets.ScrollField import ScrollField
from pathlib import Path
from kraken.containers import BaselineLine
from kraken.containers import BBoxLine

class ModelSegementationAdjustmentTab(tk.Frame):

    def __init__(self, master=None, models=[], **kwargs):
        # Call super init
        super().__init__(master, **kwargs)

        self.modelNames = models

        ## Variables
        self.trainingPath: Path = None
        self.outputPath: Path = None
        self.outputData = []
        self.imageFiles = []
        self.segmentList = []
        self.activeSegmentation = None

        # Create UI
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.initializeAllFrameData()
        self.showFrame()

        self.pack(fill='both', expand=True)

    def updateSegmentationData(self, selectedIndex):
        self.outputData = []
        self.imageFiles = []
        self.segmentList = []

        if(selectedIndex >= 0):
            self.trainingPath = Path(f"./Models/{self.modelSelection.GetSelectedText()}/training/")
            self.outputPath = Path(f"./Models/{self.modelSelection.GetSelectedText()}/output/")
            
            for file in self.trainingPath.iterdir():
                self.imageFiles.append(str(file))
                self.segmentList.append(file.stem)

            for file in self.outputPath.iterdir():
                self.outputData.append(str(file))

        self.outputSelection.setLabels(self.segmentList)

    def updateActiveSegmentation(self, selectedIndex):
        if(selectedIndex >= 0):
            self.selectedImg = tk.PhotoImage(file=self.imageFiles[selectedIndex])
            self.segmentationCanvas.create_image(0,0, image=self.selectedImg)

            #Draw segmentation etc.


    def initializeAllFrameData(self):
        #Frame Data for Add Data frame
        self.modelSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1", clickCallback=self.updateSegmentationData)
        self.outputSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1", clickCallback=self.updateActiveSegmentation)

        #Image Display
        self.imageFrame = tk.Frame(self)
        self.segmentationCanvas = tk.Canvas(self.imageFrame)      

    def showFrame(self):
        #Column 1
        self.modelSelection.grid(row=0, column=0, rowspan=1, sticky="nswe", pady=10, padx=3)
        self.modelSelection.setLabels(self.modelNames)

        self.outputSelection.grid(row=1, column=0, rowspan=2, sticky="news", pady=10, padx=3)
        self.outputSelection.setLabels(self.segmentList)

        #Column 2
        self.imageFrame.grid(column=1, row=0, columnspan=2, rowspan=3, sticky="news", padx= 3, pady = 3)
        self.segmentationCanvas.pack(fill="both", expand=True)