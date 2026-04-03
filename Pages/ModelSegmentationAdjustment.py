import tkinter as tk
from Widgets.ScrollField import ScrollField
from pathlib import Path
from PIL import Image, ImageTk
from lxml import etree
from kraken.lib import xml
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
        self.enableDrag = False
        self.dragX = 0
        self.dragY = 0
        self.minScale = 0.1
        self.maxScale = 2.0
        self.currentScale = 1.0
        self.imgID = 0
        self.selectedImg = None
        self.segementationCoords = []

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

            self.activeSegmentation = xml.XMLPage(self.outputData[selectedIndex])
            self.initializeSegementationBoxes(self.activeSegmentation)

    def updateActiveSegmentation(self, selectedIndex):
        if(selectedIndex >= 0):
            self.originalImg = Image.open(self.imageFiles[selectedIndex])
            self.selectedImg = ImageTk.PhotoImage(self.originalImg)
            self.imgID = self.segmentationCanvas.create_image(0,0, anchor="nw", image=self.selectedImg)

            self.setScale(1.0)

            #Draw segmentation etc.
            self.initializeSegementationBoxes()

    def initializeSegementationBoxes(self, segmentationData):
        if(not segmentationData == None):
            # Initialize segmentation boxes based on the active segmentation data
            pass

    def initializeAllFrameData(self):
        #Frame Data for Add Data frame
        self.modelSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1", clickCallback=self.updateSegmentationData)
        self.outputSelection = ScrollField(self, supportSelection=True, viewBG="#505050", labelBG="#B1B1B1", clickCallback=self.updateActiveSegmentation)

        #Image Display
        self.imageFrame = tk.Frame(self)
        self.segmentationCanvas = tk.Canvas(self.imageFrame)
        self.setScale(1.0)

        #Event Bindings
        self.segmentationCanvas.bind("<ButtonPress-1>", self.onCanvasClick)
        self.segmentationCanvas.bind("<B1-Motion>", self.onMouseMove)
        self.segmentationCanvas.bind("<ButtonRelease-1>", self.onCanvasRelease)
        self.segmentationCanvas.bind("<MouseWheel>", self.onZoom)      

    def showFrame(self):
        #Column 1
        self.modelSelection.grid(row=0, column=0, rowspan=1, sticky="nswe", pady=10, padx=3)
        self.modelSelection.setLabels(self.modelNames)

        self.outputSelection.grid(row=1, column=0, rowspan=2, sticky="news", pady=10, padx=3)
        self.outputSelection.setLabels(self.segmentList)

        #Column 2
        self.imageFrame.grid(column=1, row=0, columnspan=2, rowspan=3, sticky="news", padx= 3, pady = 3)
        self.segmentationCanvas.pack(fill="both", expand=True)

    def onCanvasClick(self, event):
        self.enableDrag = True
        self.dragX = event.x
        self.dragY = event.y

    def onMouseMove(self, event):
        if(self.enableDrag):
            dx = event.x - self.dragX
            dy = event.y - self.dragY

            self.segmentationCanvas.move("all", dx, dy)

            self.dragX = event.x
            self.dragY = event.y

    def onCanvasRelease(self, event):
        self.enableDrag = False
    
    def onZoom(self, event):
        if event.delta > 0:
            self.currentScale += 0.1
        else:
            self.currentScale -= 0.1

        self.setScale(self.currentScale, (event.x, event.y))

    def setScale(self, newScale, origin=(0,0)):
        
        if(newScale < self.maxScale and newScale > self.minScale):
            scaleFactor = 1 - (self.currentScale - newScale)
            #self.currentScale = max(self.minScale, min(self.maxScale, newScale))

            x = self.segmentationCanvas.canvasx(origin[0]) 
            y = self.segmentationCanvas.canvasy(origin[1])
            self.segmentationCanvas.scale("all", x, y, scaleFactor, scaleFactor)

            if(not self.selectedImg == None):
                w = int(self.originalImg.width * self.currentScale)
                h = int(self.originalImg.height * self.currentScale)

                resized = self.originalImg.resize((w, h), Image.BILINEAR)
                self.selectedImg = ImageTk.PhotoImage(resized)

                self.segmentationCanvas.itemconfig(self.imgID, image=self.selectedImg)


# 🧠 Step 1: Treat the Canvas like a Camera (not a static image)

# Right now you’re doing:

# self.segmentationCanvas.create_image(0,0, image=self.selectedImg)

# That locks you into static coordinates.

# Instead:

# Keep a reference to the image item
# Track transforms (scale + offset)
# self.image_id = self.segmentationCanvas.create_image(0, 0, anchor="nw", image=self.selectedImg)

# self.scale = 1.0
# self.offset_x = 0
# self.offset_y = 0
# 🖱️ Step 2: Add Panning (click + drag)

# Bind mouse drag:

# self.segmentationCanvas.bind("<ButtonPress-1>", self.start_pan)
# self.segmentationCanvas.bind("<B1-Motion>", self.pan)
# def start_pan(self, event):
#     self.last_x = event.x
#     self.last_y = event.y

# def pan(self, event):
#     dx = event.x - self.last_x
#     dy = event.y - self.last_y

#     self.segmentationCanvas.move("all", dx, dy)

#     self.last_x = event.x
#     self.last_y = event.y

# 👉 Key idea: move EVERYTHING ("all"), not just the image
# That way boxes later move with it automatically.

# 🔍 Step 3: Add Zoom (mouse wheel)
# self.segmentationCanvas.bind("<MouseWheel>", self.zoom)
# def zoom(self, event):
#     scale_factor = 1.1 if event.delta > 0 else 0.9

#     self.scale *= scale_factor

#     self.segmentationCanvas.scale("all", event.x, event.y, scale_factor, scale_factor)

# 👉 This scales around the mouse position — feels natural.

# 🟥 Step 4: Drawing Bounding Boxes

# You want click-drag-release behavior:

# self.segmentationCanvas.bind("<ButtonPress-3>", self.start_box)
# self.segmentationCanvas.bind("<B3-Motion>", self.update_box)
# self.segmentationCanvas.bind("<ButtonRelease-3>", self.finish_box)
# def start_box(self, event):
#     self.box_start = (event.x, event.y)
#     self.current_box = self.segmentationCanvas.create_rectangle(
#         event.x, event.y, event.x, event.y,
#         outline="red", width=2
#     )

# def update_box(self, event):
#     x0, y0 = self.box_start
#     self.segmentationCanvas.coords(self.current_box, x0, y0, event.x, event.y)

# def finish_box(self, event):
#     pass  # Save box data here
# ⚠️ Step 5: The Big Gotcha (Coordinate Systems)

# This will bite you if you ignore it:

# 👉 Canvas coordinates ≠ image coordinates once you zoom/pan.

# If you're training OCR (which you are with Kraken), you must store boxes in original image coordinates.

# So when saving:

# canvas_coords = self.segmentationCanvas.coords(self.current_box)

# # Convert back
# image_coords = [c / self.scale for c in canvas_coords]

# If you skip this, your training data will be garbage.

# 🧱 Step 6: Structure It Properly (important)

# Right now everything is inside your tab class. That won’t scale.

# Create a dedicated widget:

# class ImageCanvas(tk.Canvas):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         self.scale = 1.0
#         self.image_id = None

# Then move:

# zoom logic
# pan logic
# box drawing

# into that class.

# 👉 Your tab should only do:

# self.segmentationCanvas.load_image(path)
# 🧭 What You Should Do Next (in order)
# ✅ Refactor into ImageCanvas class
# ✅ Implement pan (move("all"))
# ✅ Implement zoom (scale("all"))
# ✅ Implement box drawing
# ✅ Convert coords back to image space
# 🚧 Later: render Kraken segmentation overlays
# 💡 One Hard Truth

# Tkinter can do this, but it’s not designed for heavy image interaction.

# If this tool grows (and it sounds like it will), eventually you may want:

# PyQt (better graphics handling)
# or even OpenCV + custom UI

# But for now? Tkinter is totally fine if you keep it structured.

# If you want, next step I can:

# Help you wire this directly into your Kraken segmentation XML
# Or build a clean ImageCanvas class you can drop in without fighting bugs for hours