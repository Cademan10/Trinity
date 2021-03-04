from Modules import *


class Spectrum(QMainWindow):
    
    def __init__(self):
        super(Spectrum,self).__init__()
        self.mainApp=QWidget()
        #Default data file
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_data.txt")
        self.newfile=""
        
        
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        
        base=os.path.basename(self.path)
        self.fileName=os.path.splitext((base))[0]
        
        #Loads data from file
        data=np.loadtxt(self.path)
        
       
        #Turns data into array
        b=np.transpose(data)
        self.x=b[0]
        self.y=b[1]
        self.plt = pg.PlotWidget()
           
        #Creates graph and makes it a historgram
        pen = pg.mkPen(color="w",width=1)
        
        
        self.plt.setLabel("left","Counts per channel")
        self.plt.setLabel("bottom","Channel")
        self.plt.setMouseEnabled(x=False,y=False)
        self.plot = self.plt.plot(self.x, self.y,pen=pen) 
        
      

        self.plt.setMenuEnabled()
        #Establishes a range for the default to data to be displayed in
        self.plt.setRange(xRange=[0,10],yRange=[0,10])
        self.setCentralWidget(self.mainApp)

  
        #Creates the Menu bar at the top
        MenuBar=self.menuBar()
        
        #Creates File section of Menu Bar
        FileMenu = MenuBar.addMenu("File")
        
        #Upload spectrum section of file menu
        loadAction=QAction("Load Spectrum File",self)
        loadAction.triggered.connect(self.NewFile)
        loadAction.setShortcut("Ctrl+N")
        FileMenu.addAction(loadAction)
        
        
        saveAction=QAction("Save Current Plot",self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.SavePlot)
        FileMenu.addAction(saveAction)
        
        #About section of file menu
        aboutAction=QAction("About",self)
        aboutAction.triggered.connect(self.About)
        aboutAction.setShortcut("Ctrl+A")
        FileMenu.addAction(aboutAction)
        
        #Exit section of file option
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.close)    
        FileMenu.addAction(exitAction)
              
        
        #Exit option for toolbar
        exitAction=QAction(QIcon(icondir+"ExitIcon.png"),"Exit",self)
        exitAction.triggered.connect(self.close)
        
        #Refresh option for toolbar
        refreshAction=QAction(QIcon(icondir+"RefreshIcon.png"),"Refresh",self)
        refreshAction.triggered.connect(self.Refresh)
    
       
        
        
        #Zoom option for toolbar
        self.zoomAction=QAction(QIcon(icondir+"ZoomInIcon.png"),"Select Region to Zoom",self,checkable=True)
        self.zoomAction.triggered.connect(self.zoomCursor)
        
        self.zoomOutAction=QAction(QIcon(icondir+"ZoomOutIcon.png"),"Zoom Out",self)
        self.zoomOutAction.triggered.connect(self.ZoomOut)
        
        
        self.perZoomInAction=QAction(QIcon(icondir+"UpIcon.png"),"Zoom in 15%",self)
        self.perZoomInAction.triggered.connect(self.PercentZoomIn)
        
        self.perZoomOutAction=QAction(QIcon(icondir+"DownIcon.png"),"Zoom out 15%",self)
        self.perZoomOutAction.triggered.connect(self.PercentZoomOut)
        
        #Full y scale option for toolbar
        self.yScale=QAction(QIcon(icondir+"YScaleIcon.png"),"Set Full Y Scale",self)
        self.yScale.triggered.connect(self.Y_Full_Scale)
        
        #Peak selection option for toolbar
        self.peakSelect=QAction(QIcon(icondir+"PeakIcon.png"),"Select Peak",self,checkable=True)
        self.peakSelect.triggered.connect(self.peakCursor)
        
        #Background selection option for toolbar
        self.backSelec=QAction(QIcon(icondir+"BackgroundIcon.png"),"Select Background",self,checkable=True)
        self.backSelec.triggered.connect(self.backCursor)
        
        #Sum option for toolbar
        self.sumAction=QAction(QIcon(icondir+"SumIcon.png"),"Frequentist Sum",self,checkable=True)
        self.sumAction.triggered.connect(self.Sum)
        
        
        #MCMC algorithm button
        self.mcmcAction=QAction(QIcon(icondir+"MCMCIcon.png"),"Bayesian Sum",self,checkable=True)
        self.mcmcAction.triggered.connect(self.MCMC)

        self.gaussFitAction=QAction(QIcon(icondir+"gaussFitIcon.png"),"Fit Gaussian",self,checkable=True)
        self.gaussFitAction.triggered.connect(self.GaussFit)


        #Log-lin Scale option for toolbar
        self.logScale=QAction(QIcon(icondir+"LogIcon.png"),"Log Scale",self,checkable=True)
        self.logScale.triggered.connect(self.LogScale)
        
        #Create test data option for toolbar
        self.testAction=QAction(QIcon(icondir+"TestIcon.png"),"Create Test Data",self)
        self.testAction.triggered.connect(self.TestData)
        

        #Creates toolbar and implements toolbar actions
        toolBar=self.addToolBar("Toolbar")
        toolBar.addAction(exitAction)
        toolBar.addAction(refreshAction)
        toolBar.addAction(self.zoomAction)
        toolBar.addAction(self.zoomOutAction)
        toolBar.addAction(self.perZoomInAction)
        toolBar.addAction(self.perZoomOutAction)
        toolBar.addAction(self.yScale)
        toolBar.addAction(self.logScale)
        toolBar.addAction(self.peakSelect)
        toolBar.addAction(self.backSelec)
        toolBar.addAction(self.sumAction)
        toolBar.addAction(self.mcmcAction)
        toolBar.addAction(self.gaussFitAction)
        toolBar.addAction(self.testAction)
        
        toolBar.setIconSize(QtCore.QSize(40, 40))

        #Side bar displaying previously uploaded files  
        self.usedFiles = QDockWidget("Previously Used Files", self)
        self.usedFiles.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        
        sideBarWidget=QWidget()
        sideLayout=QVBoxLayout()
        
        
        self.refreshSideBar=QPushButton("Clear Files",self)
        self.refreshSideBar.clicked.connect(self.RefreshSideBar)
        
        self.listWidget = QListWidget()
        self.listWidget.itemActivated.connect(self.returnFile)
        self.previous=False    
        
        
        
        sideLayout.addWidget(self.listWidget)
        sideLayout.addWidget(self.refreshSideBar)
        sideBarWidget.setLayout(sideLayout)
        
        self.usedFiles.setWidget(sideBarWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.usedFiles)

        
    
        self.setMouseTracking(True)
        

        #Creates bottom window for displaying information
        self.dataWidget = QtWidgets.QTextEdit()
        self.dataWidget.setMinimumHeight(200)
        self.dataWidget.setMaximumHeight(200)
        self.dataWidget.setReadOnly(True)

        #self.dataWidget.setMaximumWidth(1200)
        self.dataWidget.setText("Welcome!")
        
        #Creates sliders used for moving the graph vertically
        self.s1 = QSlider(Qt.Vertical)
        self.s1.setMinimum(0)
        self.s1.setMaximum(10000)
        self.s1.setValue(0)
        #self.s1.setTickPosition(QSlider.TicksRight)
        self.s1.setTickInterval(1)
        self.s1.setSingleStep(.0001)
        #Prevents slider from moving by simply clicking on it 
        self.s1.setPageStep(0)
        self.s1.valueChanged.connect(self.Move_Y)
        self.s1.setFocusPolicy(Qt.NoFocus)

        
        #Creates sliders used for moving the graph horizontally
        self.s2 = QSlider(Qt.Horizontal)
        self.s2.setMinimum(0)
        self.s2.setMaximum(10000)
        #self.s2.setTickPosition(QSlider.TicksAbove)
        self.s2.setSingleStep(.0001)
        self.s2.setTickInterval(1)
        self.s2.setPageStep(0)
        self.s2.sliderPressed.connect(self.sliderPressed)
        self.s2.sliderReleased.connect(self.sliderReleased)
        self.s2.valueChanged.connect(self.Move_X)
        self.s2.setFocusPolicy(Qt.NoFocus)
        
        #Creates a tab widget
        self.tabs = QTabWidget()
        self.tab1 = self.plt
        self.tabs.addTab(self.tab1,"Spectrum Plot")
        
        #Sets layout for the GUI
        self.grid = QGridLayout()
        

        
        self.grid.addWidget(self.dataWidget,3,1,1,2)
        self.grid.addWidget(self.tabs,1,1,1,2)
        
        self.mainApp.setLayout(self.grid)
        
        
        #Creates two lists, one to store filepaths of previously used files
        #the other to store the file names of those files
        self.previousfilepaths=[]
        self.previousfilenames=[]
 
        
        
        with np.warnings.catch_warnings():
            np.warnings.simplefilter("ignore")
    
            usedFiles=np.loadtxt("used_file_storage.txt",dtype='str')
        
        if len(usedFiles)>0:
        
                
            if len(usedFiles[0][0])>1:
                for i in range(0,len(usedFiles)):
                    self.previousfilepaths.append(usedFiles[i][1])
                    self.previousfilenames.append(usedFiles[i][0])
                    
                    self.listWidget.addItem(usedFiles[i][0])
            else:
                self.previousfilepaths.append(usedFiles[1])
                self.previousfilenames.append(usedFiles[0])
                    
                self.listWidget.addItem(usedFiles[0])
        
        self.zoomClickCounter=0
        self.zoomClickedReg=[]
        self.zoomRegStorage=[]
        
        self.peakCounter=0
        self.peakClickedRange=[]
        
        self.backCounter=0
        self.backClickedRange=[]
        self.backUsed=0
        
        
        self.incrementZoomRegStorage=[]
        self.incremented=False
        
        self.cursor_label=QLabel("Channel=0")
        self.cursor_label.setFixedWidth(150)
        self.cursor_label.setFixedHeight(15)
        self.plt.scene().sigMouseMoved.connect(self.mouseMoved)
        
        self.energy_label=QLabel("Energy=NA")
        self.energy_label.setFixedWidth(150)
        self.energy_label.setFixedHeight(21)
    
        
        
        
        
        channelLayout=QVBoxLayout(self.mainApp)
        channelLayout.addWidget(self.cursor_label)
        channelLayout.addWidget(self.energy_label)
        
        self.grid.addLayout(channelLayout,0,1)
        
        self.energyCallibrationSlope=QLineEdit(self)
        self.energyCallibrationIntercept=QLineEdit(self)
        
    
        
        energyLayout=QFormLayout(self.mainApp)
        energyLayout.addRow("Slope: ", self.energyCallibrationSlope)
        energyLayout.addRow("Intercept: ", self.energyCallibrationIntercept)
       
        self.energyCallibrationSlope.setMaximumWidth(80)
      
        self.energyCallibrationIntercept.setMaximumWidth(80)
        
       
        
        self.calibrateButton=QPushButton(self.mainApp)
        self.calibrateButton.setFixedWidth(83)
        self.calibrateButton.setFixedHeight(60)
        self.calibrateButton.clicked.connect(self.CalibrateEnergy) 
        
        
        self.energyLabel=QLabel("Calibrate Energy",self.calibrateButton)
        self.energyLabel.setWordWrap(True)
        

        
        calibrationButtonLayout=QHBoxLayout(self.calibrateButton)
        calibrationButtonLayout.addWidget(self.energyLabel,1,Qt.AlignCenter)
        
        
        
        energyButtonLayout=QHBoxLayout(self.mainApp)
        
        energyButtonLayout.addWidget(self.calibrateButton) 
        energyButtonLayout.addLayout(energyLayout)
        
        self.grid.addLayout(energyButtonLayout,0,2)
   
        self.energyCallibrationParamters=[]
        
        self.plt.hideButtons()
        
     
    

        
    def NewFile(self):
        

  

            
        #Uploads new file
        if self.previous==False:
            self.newfile=QFileDialog.getOpenFileName(None,"Spectrum Files","*.dat")[0]
            
      
        if self.previous==True:
            self.newfile=self.newfile
  
        #If no file is selected by the user, it reuploads the default data file
        if self.newfile=="":
            if len(self.previousfilenames)==0:
                self.newfile=project_directory+"\default_data.txt"
                
            #If the user decides not to upload a new file, it will simply 
            #return back to the original file with nothing changed 
            if len(self.previousfilenames)>0:
                self.newfile=self.previousfilenames[-1]
                return
            self.plt.setRange(xRange=[0,10],yRange=[0,10])
        
        #Refreshes the plot
        Spectrum.Refresh(self)
        
        newBase=os.path.basename(self.newfile)
        newFileName=os.path.splitext((newBase))[0]
        self.previousfilenames.append(newFileName)
        
        self.previousfilepaths.append(self.newfile)
        

        f=open("used_file_storage.txt","a")
        f.write(newFileName+"\t"+self.newfile+"\n")
        f.close()
            
        
        
        if self.newfile!="":
            
            log=False
            if self.logScale.isChecked()==True:
                log=True
            self.logScale.setChecked(False)
        #Sets data based on newly uploaded file
            newData=np.loadtxt(self.newfile)
            b=np.transpose(newData)
            newx=b[0]
            newy=b[1]
            self.x = newx
            #Adds an x value to the end of the graph
            #Histogram requires n+1 x-values for n y-values
            x=int(self.x[-1]+1)
            self.x=np.append(self.x,x)
            self.y =newy
            self.stored_y=self.y
            pen=pg.mkPen(color='k',width=2)
            self.plot.setData(self.x, self.y,pen=pen,stepMode=True)

            self.plt.addItem(self.plot)
            
            
        
            if log==True:
                self.logScale.setChecked(True)
                self.LogScale()  
                log=False
            
        #Automatically changes scale based on new data
            self.plt.enableAutoRange(x=True,y=True )
            self.plt.enableAutoRange(x=False,y=False)
   
      

        #Takes file name from new file
            newBase=os.path.basename(self.newfile)
            newFileName=os.path.splitext((newBase))[0]
            self.fileName=newFileName
        #Side bar that shows previously uploaded files
            self.listWidget.addItem(self.fileName)
            self.dataWidget.append("")
            self.dataWidget.append(newFileName+" uploaded")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)

            self.zoomClickCounter=0
            self.zoomClickedReg.clear()
            self.zoomRegStorage.clear()
            
        
            
            self.previous=False
            #Updates the plot
            self.plt.update()
            
            
            
            
        
        
    #Displays a message box if the user chooses the About option in the file menu
    def About(self):
        about = QMessageBox()
        about.setWindowTitle("About")
        about.setText("<font size = 5 > Welcome to Trinity! This is a program designed by Cade Rodgers for the purpose of analyzing pulse-height spectra.  </font>")
        trinityLogo=QPixmap(icondir+"TrinityLogo.png")
        about.setIconPixmap(trinityLogo.scaled(70,70,transformMode=Qt.SmoothTransformation))
        about.exec()
        
    
    
            
    def Refresh(self):
        #Removes everything from plot and unchecks all the boxes
        #Uses if statements to avoid errors if a certain object hasn't been created yet
    
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        
        
        self.mcmcAction.setEnabled(True)
        self.gaussFitAction.setEnabled(True)
        self.sumAction.setEnabled(True)
    
        
        self.peakCounter=0
        self.peakClickedRange.clear()
        
        self.backCounter=0
        self.backClickedRange.clear()
      
        
        
        try:
            self.plt.removeItem(self.totalfill)
            self.plt.removeItem(self.reg1fill)
            self.plt.removeItem(self.reg2fill)
            self.plt.removeItem(self.regplot)

        except:
            pass
        
        try:
            self.plt.removeItem(self.peakReg)
            self.plt.removeItem(self.backReg1)
            self.plt.removeItem(self.backReg2)
        except:
            pass
        
        try:
            self.plt.scene().sigMouseClicked.disconnect(self.PeakClick)
        except:
            pass
        try:
            self.plt.scene().sigMouseClicked.disconnect(self.zoomClick)
        except:
            pass
        try:
            self.plt.scene().sigMouseClicked.disconnect(self.BackClick)
        except:
            pass
            
   
        if self.mcmcAction.isChecked()==True:
            self.plt.removeItem(self.reg1fill)
            self.plt.removeItem(self.reg2fill)
            self.plt.removeItem(self.regplot)
            self.plt.removeItem(self.totalfill)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)

            
        if self.gaussFitAction.isChecked()==True:
            self.plt.clear()
            
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            self.tabs.removeTab(1)
            
            
            pen=pg.mkPen(color="k",width=2)
            self.plot.setData(self.x, self.y,pen=pen,stepMode=True)
            self.plt.addItem(self.plot)
            

            
    #Unchecks many of the tabs

        self.peakSelect.setChecked(False)
        self.sumAction.setChecked(False)
        self.backSelec.setChecked(False)
        self.mcmcAction.setChecked(False)
        self.gaussFitAction.setChecked(False)
        
        self.dataWidget.append("""
Viewing window cleared""")
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)

     
            
   
    def mouseMoved(self,evt):
        pos = evt
        if self.plt.sceneBoundingRect().contains(pos):
            mousePoint = self.plt.plotItem.vb.mapSceneToView(pos)
            if mousePoint.x()<self.x[0]:
                x=self.x[0]
            elif mousePoint.x()>self.x[-1]:
                x=self.x[-1]
            else:
                x=mousePoint.x()
                
            if mousePoint.y()>int(np.max(self.y)):
                y=np.max(self.y)
            elif mousePoint.y()<int(np.min(self.y)):
                y=np.min(self.y)
            else:
                y=mousePoint.y()
                
            self.posX=x
            self.posY=y
            
            self.cursor_label.setText("Channel=" +str(int(round(x))))
            
            
            if len(self.energyCallibrationParamters)!=0:
                energySlope=self.energyCallibrationParamters[0][0]
                energyIntercept=self.energyCallibrationParamters[0][1]
                channel=int(round(x))
                
                ##Energy calibrated according to the equation
                #Energy = channel*slope + intercept
                channelEnergy=round(energySlope*channel+energyIntercept,2)
                self.energy_label.setText("Energy="+str(channelEnergy))
            
           
            
            if self.zoomAction.isChecked()==True:
                                  
                if self.zoomClickCounter==1:
                    self.zoomReg.setRegion((self.zoomClickedReg[0],self.posX))
            
            if self.peakSelect.isChecked()==True and self.backSelec.isChecked()==False:
                if self.peakCounter==1:
                    self.peakReg.setRegion((self.peakClickedRange[0],self.posX))
                    
            if self.backSelec.isChecked()==True:
                if self.backCounter==1:
                    self.backReg1.setRegion((self.backClickedRange[0],self.posX))
                if self.backCounter==3:
                    self.backReg2.setRegion((self.backClickedRange[2],self.posX))
    
    def zoomCursor(self):
        if self.newfile!="":
            
            if self.peakSelect.isChecked()==True or self.backSelec.isChecked()==True:
                self.zoomAction.setChecked(False)
                

            
            QApplication.setOverrideCursor(Qt.CrossCursor)
            
            if self.zoomAction.isChecked()==True:
                self.plt.scene().sigMouseClicked.connect(self.zoomClick)
                       
        
        
        if self.newfile=="":
            self.zoomAction.setChecked(False)
  
            
        if self.zoomAction.isChecked()==False:
           
                
                
            
            if self.peakCounter>1 or self.backCounter>1==True:
                pass

            
            
            
            if self.peakCounter==0 and self.backCounter==0:
                QApplication.setOverrideCursor(Qt.ArrowCursor)
            
            if self.zoomClickCounter==1:
                self.plt.removeItem(self.zoomReg)
                
                QApplication.setOverrideCursor(Qt.ArrowCursor)
                
                self.zoomClickCounter=0
                self.zoomClickedReg.clear()
            
            try:
                self.plt.scene().sigMouseClicked.disconnect(self.zoomClick)
            except:
                pass
            
            
            
    def ZoomOut(self):
        self.incrementZoomRegStorage.clear()
        self.zoomRegStorage.clear()
        if self.logScale.isChecked()==True:
            try:
                self.plt.setRange(xRange=[self.x[0],self.x[-1]],yRange=[np.log10(min(self.y)),np.log10(max(self.y))])
                
            except:
                self.plt.setRange(xRange=[self.x[0],self.x[-1]],yRange=[np.log10(.1),np.log10(max(self.y))])
        elif self.logScale.isChecked()==False:
            self.plt.setRange(xRange=[self.x[0],self.x[-1]],yRange=[min(self.y),max(self.y)])
            
        self.s1.setHidden(True)
        self.s2.setHidden(True)
        self.dataWidget.append(
"""
Expanded to full view""")
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)

    
    def zoomClick(self,QMouseEvent):

        if self.zoomAction.isChecked()==True:
            if QMouseEvent.button() == Qt.LeftButton:
                
                
                
                self.zoomClickedReg.append(int(round(self.posX)))
                
                self.zoomClickCounter+=1
        
                
                if self.zoomClickCounter==1:
                    self.zoomReg=pg.LinearRegionItem(values=(self.posX,self.posX),movable=False)
                    self.plt.addItem(self.zoomReg)
                
                
               
                if self.zoomClickCounter==2:
                           
                    #Creates sliders to move along axes
                    
                    self.grid.addWidget(self.s1,1,0)
                    self.grid.addWidget(self.s2,2,1,1,2)
                    self.s1.setHidden(False)
                    self.s2.setHidden(False)
                
                    if self.zoomClickedReg[0]<self.zoomClickedReg[1]:
                        self.minx=int(round(self.zoomClickedReg[0]))
                 #The last x value of the selected region   
                        self.maxx=int(round(self.zoomClickedReg[1]))
                        
                    if self.zoomClickedReg[0]>self.zoomClickedReg[1]:
                        self.minx=int(round(self.zoomClickedReg[1]))
                 #The last x value of the selected region   
                        self.maxx=int(round(self.zoomClickedReg[0]))
                    
                    if self.zoomClickedReg[0]==self.zoomClickedReg[1]:
                        self.minx=self.zoomClickedReg[0]
                        self.maxx=self.zoomClickedReg[0]+10
                        
              
                    
                    self.yvals=self.y[int(self.minx-self.x[0]):int(self.maxx-self.x[0])]
               
                    self.stored_yvals=self.stored_y[self.minx:self.maxx]
                    
                #Maximum y value in the select region
                    self.Ymax=np.amax(self.yvals)
      
                    
                    self.stored_Ymax=np.amax(self.yvals)
                    
                    
                    
                    self.Ymax=np.amax(self.yvals)
                    
        
        
        
                    self.y_max=np.amax(self.y)
                    
                    self.y_start=(10001*self.Ymax-10000*min(self.yvals))/(self.Ymax-min(self.yvals))
                    self.y_inc=(max(self.yvals)-min(self.yvals))/10001
                    self.y_value=self.y_start
                    
                    

                    
                    
                    self.s1.setValue(self.y_value)





                    self.x_max=np.amax(self.x)
                    x_ran=self.x[-1]-self.x[0]
                    


                    self.x_avg=self.maxx-self.minx
                    
                    
                    
                    
                    m=(self.x[-1]-self.x[0]-self.x_avg)/self.x_avg
                    
                    
            
                    
                    
                    self.start=10000*((self.minx-self.x[0])/(self.x_avg))/m
           
                    self.increment=(m*self.x_avg)/10000
                         
               
                    self.s2.setValue(int(round(self.start)))
                    
                
                    self.zoomRegStorage.append([self.minx,self.maxx,self.Ymax,self.Ymax])
                    
                    self.incrementZoomRegStorage.clear()
                    self.incrementZoomRegStorage.append([self.minx,self.maxx,self.Ymax])
                    
                
                #Takes input from SelectRegion method to set the plot's range
                    self.plt.setRange(xRange=[self.minx,self.maxx])
                    
            
                        
                    self.plt.setRange(yRange=[np.amin(self.yvals),self.Ymax])
                    
                    


                    self.dataWidget.append(
"""
Region between Channel """ + str(int(self.minx)) +" and Channel " + str(int(self.maxx))+ " selected")
                    self.dataWidget.moveCursor(QtGui.QTextCursor.End)
        

                    self.zoomClickCounter=0
                    self.plt.removeItem(self.zoomReg)
                
                    self.plt.scene().sigMouseClicked.disconnect(self.zoomClick)
                
                    self.zoomClickedReg.clear()
                    QApplication.setOverrideCursor(Qt.ArrowCursor)
                    
                    if self.logScale.isChecked()==True:
                        if min(self.yvals)>0:
                            self.plt.setRange(yRange=[np.log10(np.amin(self.yvals)),np.log10(self.Ymax)])
                   
                        else:
                            self.plt.setRange(yRange=[np.log10(.1),np.log10(self.Ymax)])
                    self.zoomAction.setChecked(False)
                    
                    self.prevMins1=[self.minx]
                
                    self.prevMins2=[self.minx]
                    
                    if len(self.zoomRegStorage)>1:
                        self.offset=self.minx-self.zoomRegStorage[-2][0]
                    
                    self.prevYMins=[self.Ymax]
                    self.prevYMins1=[self.Ymax]
     
                    
    def Midpoint(self,data):
        midChan=int(round((data[-1]+data[0])/2))
        
        return midChan
        
        
        
        
    def PercentZoomIn(self):
        if self.newfile=="":
            return 0
        
        
        if len(self.incrementZoomRegStorage)==0:
            
            
            midChan=self.Midpoint(self.x)
            
            reducedChanRange=int(round(.85*(self.x[-1]-self.x[0])))
            
            
            
        elif len(self.incrementZoomRegStorage)==1:
            minx=self.incrementZoomRegStorage[-1][0]
            maxx=self.incrementZoomRegStorage[-1][1]
            midChan=self.Midpoint([minx,maxx])
            
            reducedChanRange=int(round(.85*(maxx-minx)))
            
            
    
        reducedChanRangePerSide=reducedChanRange/2
        
        
        
        self.minx=midChan-reducedChanRangePerSide
        self.maxx=midChan+reducedChanRangePerSide
        
        self.x_max=np.amax(self.x)
        x_ran=self.x[-1]-self.x[0]
                    


        self.x_avg=self.maxx-self.minx
                    
        self.yvals=self.y[int(self.minx-self.x[0]):int(self.maxx-self.x[0])]
        
               
                    
                #Maximum y value in the select region
        self.Ymax_reg=np.amax(self.yvals)
                    
        
        
      
        self.grid.addWidget(self.s1,1,0)
        self.s1.setHidden(False)

        if len(self.zoomRegStorage)==0:
            self.y_start=(10001*self.Ymax_reg-10000*min(self.yvals))/(max(self.yvals)-min(self.yvals))
            self.y_inc=(max(self.yvals)-min(self.yvals))/10001
            self.y_value=self.y_start
            
            
            self.s1.setValue(self.y_value)
            
             
                    
        m=(self.x[-1]-self.x[0]-self.x_avg)/self.x_avg
                    
            
                    
        self.start=10000*((self.minx-self.x[0])/(self.x_avg))/m
                    
        self.increment=(m*self.x_avg)/10000
                  
        self.grid.addWidget(self.s2,2,1,1,2)
        self.s2.setHidden(False)
        self.s2.setValue(int(round(self.start)))
    
        
        
        self.plt.setRange(xRange=[midChan-reducedChanRangePerSide,midChan+reducedChanRangePerSide])
        
        self.incrementZoomRegStorage.clear()
        self.incrementZoomRegStorage.append([midChan-reducedChanRangePerSide,midChan+reducedChanRangePerSide,self.Ymax_reg])   
        
        
        if len(self.zoomRegStorage)==0:
            self.zoomRegStorage.append([midChan-reducedChanRangePerSide,midChan+reducedChanRangePerSide,self.Ymax_reg,self.Ymax_reg])   
        
        else:
          self.zoomRegStorage[-1]=[midChan-reducedChanRangePerSide,midChan+reducedChanRangePerSide,self.Ymax_reg,self.Ymax_reg]
        
        
        
    def PercentZoomOut(self):
        if len(self.incrementZoomRegStorage)==0:
            pass
        
        
        if len(self.incrementZoomRegStorage)==1:
            minx=self.incrementZoomRegStorage[-1][0]
            maxx=self.incrementZoomRegStorage[-1][1]
            midChan=self.Midpoint([minx,maxx])
            
            expandedChanRange=int(round(1.15*(maxx-minx)))
            
            

            expandedChanRangePerSide=expandedChanRange/2
        
            
        
            self.minx=midChan-expandedChanRangePerSide
            self.maxx=midChan+expandedChanRangePerSide
            
            if self.maxx>=self.x[-1]:
                self.maxx=self.x[-1]
            if self.minx<=self.x[0]:
                self.minx=self.x[0]
            
            
            if self.maxx-self.minx>=self.x[-1]-self.x[0]:
                self.incrementZoomRegStorage.clear() 
                self.zoomRegStorage.clear()
                self.s2.setHidden(True)
                self.s1.setHidden(True)
                
                self.plt.setRange(xRange=[self.x[0],self.x[-1]],yRange=[min(self.y),max(self.y)])
                
                
            
            
            else:
                self.x_max=np.amax(self.x)
                x_ran=self.x[-1]-self.x[0]
                    


                self.x_avg=self.maxx-self.minx
                        
                self.yvals=self.y[int(self.minx-self.x[0]):int(self.maxx-self.x[0])]
   
                #Maximum y value in the select region
                self.Ymax_reg=np.amax(self.yvals)
                    
                m=(self.x[-1]-self.x[0]-self.x_avg)/self.x_avg
                    
            
                    
                self.start=10000*((self.minx-self.x[0])/(self.x_avg))/m
                    
                self.increment=(m*self.x_avg)/10000
                  
        
        
        
        
                self.plt.setRange(xRange=[self.minx,self.maxx])
        
                self.incrementZoomRegStorage.clear()
                self.incrementZoomRegStorage.append([self.minx,self.maxx,self.Ymax_reg])   
                self.zoomRegStorage.append([self.minx,self.maxx,self.Ymax_reg,self.Ymax_reg])   
                
                if len(self.zoomRegStorage)>1:
                    if self.zoomRegStorage[-2][1]-self.zoomRegStorage[-1][0]<=self.maxx-self.minx:
                        self.zoomRegStorage.pop(-1)
            
     
        
     
        
     
    def Move_X(self, value):
        
  
        
      self.xvar=(value-self.start)*self.increment
        
      self.plt.setRange(xRange=[self.minx+self.xvar,self.maxx+self.xvar])
      
      if self.minx+self.xvar<self.x[0]:
            self.plt.setRange(xRange=[self.x[0],self.maxx+self.xvar])
      if self.maxx+self.xvar>self.x[-1]:
            self.plt.setRange(xRange=[self.minx+self.xvar,self.x[-1]])
     
        
           
        
     
        
         
    

    
                
    def sliderPressed(self):
        self.pressed=True
        self.startSlideVal=self.s2.value()
        
        
    def sliderReleased(self):
        
        if self.pressed==True:
            self.endSlideVal=self.s2.value()
        
            
            
            xChange=self.increment*(self.endSlideVal-self.startSlideVal)

            
            self.incrementZoomRegStorage[-1][0]+=xChange
            self.incrementZoomRegStorage[-1][1]+=xChange
            
    
            
            if self.endSlideVal==0:
                offset=self.incrementZoomRegStorage[-1][0]-self.x[0]
                
                self.incrementZoomRegStorage[-1][0]-=offset
                self.incrementZoomRegStorage[-1][1]-=offset
            
            if self.endSlideVal==100000:
                offset=self.x[-1]-self.incrementZoomRegStorage[-1][1]
                
                self.incrementZoomRegStorage[-1][0]+=offset
                self.incrementZoomRegStorage[-1][1]+=offset
            
            #Obtains the largest count in the new region to use as the new maximum
            #count value for the region 
            
            changedYMax=max(self.y[int(round(self.incrementZoomRegStorage[-1][0]-self.x[0])):int(round(self.incrementZoomRegStorage[-1][1]-self.x[0]))+1])

           
            self.incrementZoomRegStorage[0][-1]=changedYMax
            self.pressed=False
        else:
            pass
              
            
                
 
    
        
    def Move_Y(self, value):
        
        if len(self.zoomRegStorage)>=1 or len(self.incrementZoomRegStorage)>=1:
            
            
            
            
            y=self.y_inc*(value-self.y_start)
            
            if self.logScale.isChecked()==True:
                
                if min(self.yvals)>0:
                    self.plt.setRange(yRange=[np.log10(np.amin(self.yvals)),np.log10(self.Ymax+y)])
                   
                else:
                    self.plt.setRange(yRange=[np.log10(.1),np.log10(self.Ymax+y)])
            
                
            

                
            else:
                self.plt.setRange(yRange=[min(self.yvals),self.Ymax+y])
        
           
            self.ChangedYMax=self.Ymax+y
            if len(self.zoomRegStorage)>=1:
                try:
                    change=self.Ymax+y-(self.prevYMins[0])
                    self.prevYMins[0]=self.Ymax+y
                    self.zoomRegStorage[-1][2]+=change
                except:
                    pass
 
            
        
    def Y_Full_Scale(self):
        if len(self.incrementZoomRegStorage)==0:
            pass
        if len(self.incrementZoomRegStorage)>0:
        
            x_min=int(self.incrementZoomRegStorage[0][0]-self.x[0])
            x_max=int(self.incrementZoomRegStorage[0][1]-self.x[0])+1
        
            self.yvals=self.y[x_min:x_max]
 #Sets y scale to the maximum y value of the spectrum
            maximum_y=self.incrementZoomRegStorage[0][-1]
            if maximum_y>=max(self.y):
                maximum_y=max(self.y)
            min_y=min(self.yvals)
        
        
        
            self.Ymax=maximum_y
            self.ChangedYMax=maximum_y
            self.y_inc=(max(self.yvals)-min(self.yvals))/10001
            self.y_start=int(round(((10001*maximum_y-10000*min_y)/(maximum_y-min_y))))
                
            
                    
            self.s1.setValue(self.y_start)
        
        
            if self.logScale.isChecked()==True:
                maximum_y=np.log10(maximum_y)
      
            
                if min(self.yvals)<=0:
                
                    min_y=np.log10(.1)
                if min(self.y)>0:
                    min_y=np.log10(min(self.yvals))
       
            self.plt.setRange(yRange=[min_y,maximum_y])
      
        
      
                
      
        self.dataWidget.append(
"""
Y-axis set to full scale""")
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
        self.yScale.setChecked(False)
        
        
        
        
    def LogScale(self):
        if self.logScale.isChecked()==True:
            self.dataWidget.append(
"""
Converted to Log Scale""")    

            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                
            logy=[]
  
            for i in range(len(self.y)):
                if self.y[i]<=0:
                    logy.append(.1)
                else:
                    logy.append(self.y[i])
                    
            logx=self.x
            pen=pg.mkPen(color='k',width=2)
         
            if self.newfile!="":
                self.plot.setData(logx, logy,pen=pen,stepMode=True)
                self.plt.setLogMode(False,True) 
            
            if len(self.incrementZoomRegStorage)>=1:
                
            
                xmin=self.incrementZoomRegStorage[-1][0]-self.x[0]
                xmax=self.incrementZoomRegStorage[-1][1]-self.x[0]
                
                
             
                
                
                try:
                    Ymax=self.ChangedYMax
                except:
                    Ymax=self.incrementZoomRegStorage[-1][-1]
                y_min=min(self.y[int(round(xmin)):int(round(xmax))+1])
                
                try:
                    self.plt.setRange(yRange=[np.log10(y_min),np.log10(Ymax)])
                except:
                    self.plt.setRange(yRange=[np.log10(.1),np.log10(Ymax)])
                self.plt.setRange(xRange=[xmin+self.x[0],xmax+self.x[0]])

            

            
   
            if self.sumAction.isChecked()==True or self.mcmcAction.isChecked()==True:
                y=[]
                for i in range(len(self.peaky)):
                    if self.peaky[i]<=0:
                        y.append(.1)
                    else:
                        y.append(np.log10(self.peaky[i]))
                
                
                x=self.peakx
                x=np.append(x,x[-1]+1)
                self.plt.removeItem(self.totalfill)
                color=pg.mkColor(0,255,255,50)
                pen=pg.mkPen(color="k",width=2)
                brush=pg.mkBrush(color=color)

                self.totalfill.setData(x,y,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                self.plt.addItem(self.totalfill)
                
                
                names=[item.name() for item in self.plt.listDataItems()]
                if "reg1fill" in names:
                    y1=[]
                    y2=[]
                    for i in range(len(self.reg1yrange)):
                        if self.reg1yrange[i]<=0:
                            y1.append(.1)
                        else:
                            y1.append(np.log10(self.reg1yrange[i]))
                            
                    for i in range(len(self.reg2yrange)):
                        if self.reg2yrange[i]<=0:
                            y2.append(.1)
                        else:
                            y2.append(np.log10(self.reg2yrange[i]))
                    
                    x1=self.x1range 
                    
                    while len(x1)<=len(y1):
                        x1=np.append(x1,x1[-1]+1)
                    
                    x2=self.x2range 
                    
                    while len(x2)<=len(y2):   
                        x2=np.append(x2,x2[-1]+1)
                    
                    color=pg.intColor(0, alpha=50)
                    pen=pg.mkPen(color="k",width=2)
    
                    brush=pg.mkBrush(color=color)
                    self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                    
                    self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
        
        if self.logScale.isChecked()==False:
            self.dataWidget.append(
"""
Converted to Linear Scale""")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
            pen=pg.mkPen(color='k',width=2)
            if self.newfile!="":
                self.plot.setData(self.x, self.y,pen=pen,stepMode=True)
                self.plt.setLogMode(False,False)
                
                self.plt.setRange(yRange=[min(self.y),max(self.y)])
                
            if len(self.incrementZoomRegStorage)>=1:
                
                xmin=self.incrementZoomRegStorage[-1][0]-self.x[0]
                xmax=self.incrementZoomRegStorage[-1][1]-self.x[0]

                
                try:
                    Ymax=self.ChangedYMax
                except:
                    Ymax=self.incrementZoomRegStorage[-1][-1]
                y_min=min(self.y[int(round(xmin)):int(round(xmax))+1])
                
                
                self.plt.setRange(yRange=[y_min,Ymax])
       
                self.plt.setRange(xRange=[xmin+self.x[0],xmax+self.x[0]])

                   
            
            if self.sumAction.isChecked()==True or self.mcmcAction.isChecked()==True:
                self.plt.removeItem(self.totalfill)
                color=pg.mkColor(0,255,255,50)
                pen=pg.mkPen(color="k",width=2)
                brush=pg.mkBrush(color=color)
                x=self.peakx
                x=np.append(x,x[-1]+1)
                self.totalfill.setData(x,self.peaky,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                self.plt.addItem(self.totalfill)
                
                
                
                names=[item.name() for item in self.plt.listDataItems()]
                if "reg1fill" in names:
                    x1=self.x1range 
                    y1=self.reg1yrange
                    while len(x1)<=len(y1):
                        x1=np.append(x1,x1[-1]+1)
                    x2=self.x2range
                    y2=self.reg2yrange
                    while len(x2)<=len(y2):
                        x2=np.append(x2,x2[-1]+1)
                  
                    
                    color=pg.intColor(0, alpha=50)
                    pen=pg.mkPen(color="k",width=2)
    
                    brush=pg.mkBrush(color=color)
                    self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)

                    self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                
     
                
     
        
    def peakCursor(self):
        if self.newfile!="":
            
            if self.peakSelect.isChecked()==True:
                
                if self.zoomAction.isChecked()==True:
                    self.peakSelect.setChecked(False)
                
                self.plt.scene().sigMouseClicked.connect(self.PeakClick)
                
                if self.sumAction.isChecked()==True or self.mcmcAction.isChecked()==True:
                    self.mcmcAction.setEnabled(True)
                    self.gaussFitAction.setEnabled(True)
                    self.sumAction.setEnabled(True)
                    
                    
                    self.plt.removeItem(self.totalfill)
                    
                    if self.sumAction.isChecked()==True:
            
                        self.sumAction.setChecked(False)
                    
                        
                    if self.mcmcAction.isChecked()==True:
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.mcmcAction.setChecked(False)
                        
                    self.backSelec.setChecked(False)
                    
                    try:
                        self.plt.removeItem(self.reg1fill)
                        self.plt.removeItem(self.reg2fill)
                        self.plt.removeItem(self.regplot)
                    except:
                        pass
                elif self.gaussFitAction.isChecked()==True:
                    self.plt.scene().sigMouseClicked.disconnect(self.PeakClick)
                    
                    
                
                    self.mcmcAction.setEnabled(True)
                    self.gaussFitAction.setEnabled(True)
                    self.sumAction.setEnabled(True)
              
                    pen=pg.mkPen(color="k",width=2)
                    self.plt.clear()
                    self.plot.setData(self.x, self.y,pen=pen,stepMode=True)
                    self.plt.addItem(self.plot)
                    
            
                
        
   
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                     
                    self.backSelec.setChecked(False)
                    self.gaussFitAction.setChecked(False)
                    
                    self.plt.scene().sigMouseClicked.connect(self.PeakClick)
                    
                if self.backSelec.isChecked==True:
                    try:
                 
                        self.plt.removeItem(self.backReg1)
                        self.plt.removeItem(self.backReg2)

                        self.backSelec.setChecked(False)
                       
                    except:
                        pass
                    
            QApplication.setOverrideCursor(Qt.CrossCursor)
            
        if self.newfile=="":
            self.dataWidget.append(
"""
Upload file first""")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
            self.peakSelect.setChecked(False)
            
        if self.peakSelect.isChecked()==False:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            try:
                self.plt.scene().sigMouseClicked.disconnect(self.PeakClick)
            except:
                pass
            self.peakCounter=0
            self.peakClickedRange.clear()  
     
            
             
            
            
            try:
                self.plt.removeItem(self.peakReg)
                self.plt.removeItem(self.backReg1)
                self.plt.removeItem(self.backReg2)
                self.backCounter=0
   
                self.backClickedRange.clear()  
                self.backSelec.setChecked(False)
                
                
            except:
                self.backCounter=0
   
                self.backClickedRange.clear()
    
                self.backSelec.setChecked(False)
            try:
                self.plt.scene().sigMouseClicked.disconnect(self.BackClick)
            except:
                pass
            
            
        
            
            
        
    def PeakClick(self,QMouseEvent):
        if self.peakSelect.isChecked()==True:
            if QMouseEvent.button() == Qt.LeftButton:
                
                
                
                self.peakClickedRange.append(int(round(self.posX)))
                
        
                
                if self.peakCounter==0:
                    self.peakReg=pg.LinearRegionItem(values=(self.posX,self.posX),movable=False)
                    color=pg.mkColor(0,255,255,70)
                    brush=pg.mkBrush(color=color)

                    self.peakReg.setBrush(brush)
                    
                    self.plt.addItem(self.peakReg)
                
                self.peakCounter+=1
                
                if self.peakCounter==2:
                    
                  
                    
                    if self.peakClickedRange[0]<self.peakClickedRange[1]:
                        self.xmin=int(round(self.peakClickedRange[0]))
                 #The last x value of the selected region   
                        self.xmax=int(round(self.peakClickedRange[1]))
                        
                    if self.peakClickedRange[0]>self.peakClickedRange[1]:
                        self.xmin=int(round(self.peakClickedRange[1]))
                 #The last x value of the selected region   
                        self.xmax=int(round(self.peakClickedRange[0]))
                    
                    if self.peakClickedRange[0]==self.peakClickedRange[1]:
                        self.xmin=self.peakClickedRange[0]
                        self.xmax=self.peakClickedRange[0]+10
                

   
                    firstIndex=int(round(self.xmin))-int(round(self.x[0]))
                    lastIndex=int(round(self.xmax))-int(round(self.x[0]))

              
                    self.firsty=self.y[firstIndex]
                    self.lasty=self.y[lastIndex]

                    #List of all the x and y values within the selected region
                    self.peakx=self.x[firstIndex:lastIndex+1]
                    self.peaky=self.y[firstIndex:lastIndex+1]     
                    
                    self.peakCounter=0
                    self.peakClickedRange.clear()  
                    self.plt.scene().sigMouseClicked.disconnect(self.PeakClick)
                    QApplication.setOverrideCursor(Qt.ArrowCursor)
                  
    def backCursor(self):
        if self.peakSelect.isChecked()==False:

            names=[item.name() for item in self.plt.listDataItems()]
            if "reg1fill" in names:
                
                try:
                    
        
                    self.mcmcAction.setEnabled(True)
                    self.gaussFitAction.setEnabled(True)
                    self.sumAction.setEnabled(True)
                    
                    self.plt.removeItem(self.totalfill)
                    self.plt.removeItem(self.reg1fill)
                    self.plt.removeItem(self.reg2fill)
                    self.plt.removeItem(self.regplot)
                
                    self.plt.addItem(self.peakReg)
                
    
                
                    self.peakSelect.setChecked(True)

                    self.backSelec.setChecked(True)
                    self.sumAction.setChecked(False)
                    
                
                        

                    
           
                except:
                    
                    pass
        
                try:

                    
                    if self.mcmcAction.isChecked()==True:
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.tabs.removeTab(1)
                        self.mcmcAction.setChecked(False)
                except:
                    pass
                
            elif "gaussFit" in names:
    

                pen=pg.mkPen(color="k",width=2)
                
                
                self.plt.clear()
                self.plot.setData(self.x, self.y,pen=pen,stepMode=True)
                self.plt.addItem(self.plot)
              
                
                self.plt.addItem(self.peakReg)
   
    

                self.mcmcAction.setEnabled(True)
                self.gaussFitAction.setEnabled(True)
                self.sumAction.setEnabled(True)
                    
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                     

                
                self.peakSelect.setChecked(True)
                self.backSelec.setChecked(True)
                self.gaussFitAction.setChecked(False)
                
            else:
                self.dataWidget.append(
"""
Select Peak first""")
                self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                self.backSelec.setChecked(False)
            
        if self.newfile!="" and self.peakSelect.isChecked()==True:
            QApplication.setOverrideCursor(Qt.CrossCursor)
            
            if self.backSelec.isChecked()==True:
                self.plt.scene().sigMouseClicked.connect(self.BackClick)
  
        

            
        if self.backSelec.isChecked()==False:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.backCounter=0
            self.backClickedRange.clear()

            
            try:
                self.plt.scene().sigMouseClicked.disconnect(self.BackClick)
            except:
                pass
            
            try:
                self.plt.removeItem(self.backReg1)
                self.plt.removeItem(self.backReg2)
                
            except:
                pass
                
            
   
            
            
        
    def BackClick(self,QMouseEvent):
        if self.backSelec.isChecked()==True:
            if QMouseEvent.button() == Qt.LeftButton:
                
                
                
                self.backClickedRange.append(int(round(self.posX)))
                
        
                color=pg.intColor(0, alpha=70)
                brush=pg.mkBrush(color=color)
                
                if self.backCounter==0:
                    self.backReg1=pg.LinearRegionItem(values=(self.posX,self.posX),movable=False)
              
    

                    self.backReg1.setBrush(brush)
                    
                    self.plt.addItem(self.backReg1)
                    
                if self.backCounter==2:
                    self.backReg2=pg.LinearRegionItem(values=(self.posX,self.posX),movable=False)

                    self.backReg2.setBrush(brush)
                    
                    self.plt.addItem(self.backReg2)
                
                self.backCounter+=1
            
                if self.backCounter==4:
                    
                    if self.backClickedRange[0]<self.backClickedRange[1]:
                        self.reg1xmin=self.backClickedRange[0]
                        self.reg1xmax=self.backClickedRange[1]
                        
                    if self.backClickedRange[0]>self.backClickedRange[1]:
                        self.reg1xmin=self.backClickedRange[1]
                        self.reg1xmax=self.backClickedRange[0]
                    
                    reg1xmin=int(round(self.reg1xmin))
                    reg1xmax=int(round(self.reg1xmax))

                        
                    firstX=int(round(self.x[0]))
                    self.x1range=self.x[reg1xmin-firstX:(reg1xmax-firstX)+1]
                    
       
                    
                    #Y-values of the channels within the 1st region
                    self.reg1yrange=self.y[reg1xmin-firstX:(reg1xmax-firstX)+1]  
      #######################################              

                    #Gets the average count per channel of the 1st region
                    self.reg1avgy=np.sum(self.reg1yrange)/len(self.x1range) 


                    #Gets the range of channels from the 2nd region
                    
                    
                    if self.backClickedRange[2]<self.backClickedRange[3]:
                        self.reg2xmin=self.backClickedRange[2]
                        self.reg2xmax=self.backClickedRange[3]
                        
                    if self.backClickedRange[2]>self.backClickedRange[3]:
                        self.reg2xmin=self.backClickedRange[3]
                        self.reg2xmax=self.backClickedRange[2]
                    
                    
                    reg2xmin=int(round(self.reg2xmin))
                    reg2xmax=int(round(self.reg2xmax))

                    
        
                    self.x2range=self.x[reg2xmin-firstX:(reg2xmax-firstX)+1]    
                    
         
                    
                
                    self.reg2yrange=self.y[reg2xmin-firstX:(reg2xmax-firstX)+1]  
   
                    #Y values of the channels within the 2nd region
                    self.reg2avgy=np.sum(self.reg2yrange)/len(self.x2range)
    ###############################################            
  
                    
                   
                    
                    #Creates a list of two points, one being the first channel of the first region, the second being the last channel of the second region
                    self.backgroundx=[np.mean(self.x1range),np.mean(self.x2range)]
                    
                    #Creates a list of two points, one being the average y-value per channel of the first region, the second being the averag y-alue per channel of the second region
                    self.backgroundy=[self.reg1avgy,self.reg2avgy] 
                
                    x1=self.x1range
                    y1=self.reg1yrange
       
                    
                    self.y_tot_avg=(self.reg1avgy+self.reg2avgy)/2
                 
                    
                    color=pg.intColor(0, alpha=50)
                    pen=pg.mkPen(color="k",width=2)
                    linepen=pg.mkPen(color="r")
                    brush=pg.mkBrush(color=color)
                    #Fills in the first selected region
                    
                    self.reg1fill=pg.PlotCurveItem(name="reg1fill")
                
           

                    x1=np.append(x1,x1[-1]+1)
                    if len(x1)==len(y1):
                        x1=np.append(x1,x1[-1]+1)
        
                    
                    self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                    
                    
                    x2=self.x2range 
                    y2=self.reg2yrange
             
                    
                    #Fills in the second selected region
                    self.reg2fill=pg.PlotCurveItem(name="reg2fill")
                   
                    x2=np.append(x2,x2[-1]+1)
                    self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                    
                    #Creates a line connecting the points created above
                    self.regplot=pg.PlotDataItem(self.backgroundx,self.backgroundy,pen=linepen,name="self.regplot")                    
        
     
                    self.backCounter=0
                    self.backUsed=0
                    self.backClickedRange.clear()  
                    self.plt.scene().sigMouseClicked.disconnect(self.BackClick)
                    QApplication.setOverrideCursor(Qt.ArrowCursor)
     
     
                
                
    def Sum(self,PeakSelect):
        if self.sumAction.isChecked()==True:
            
            if self.peakSelect.isChecked()==False:
                self.dataWidget.append(
"""
Select peak first!""")
                self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                self.sumAction.setChecked(False)
    
            

           
            
            if self.mcmcAction.isChecked()==True:
                self.mcmcAction.setChecked(False)
                self.sumAction.setChecked(False)
                
            if self.gaussFitAction.isChecked()==True:
                self.gaussFitAction.setChecked(False)
                self.sumAction.setChecked(False)
            
        
            
            
            if self.peakSelect.isChecked()==True:
                self.mcmcAction.setEnabled(False)
                self.gaussFitAction.setEnabled(False)
                self.backUsed=0
                self.plt.removeItem(self.peakReg)
                
                
                #X and Y assigned the values within the selected peak
                x=self.peakx
                y=self.peaky
                
                color=pg.mkColor(0,255,255,50)
                pen=pg.mkPen(color="k",width=2)
                brush=pg.mkBrush(color=color)
                
                
                #Fills in the selected peak
                self.totalfill= pg.PlotCurveItem(name="totalFill")
                x=np.append(x,x[-1]+1)
                if self.logScale.isChecked()==True:
                    y=np.log10(y)
                self.totalfill.setData(x,y,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                
                self.plt.addItem(self.totalfill)
                
                
                #Removes the region selector 
          
                
                #Sums all the y values in the selected peak
                totalsum=np.sum(self.peaky)
                
                firstchannel=int(self.peakx[0])
                lastchannel=int(self.peakx[-1])
                
                #The mean channel of the selected region
                x_mean=np.multiply(self.peaky,self.peakx)
                self.x_mean=np.sum(x_mean)/np.sum(self.peaky)
                
                #Standard error of the mean channel found by dividing the standard deviation by the square root of the total count 
                x_squared=(self.peakx-self.x_mean)**2
                xy=np.multiply(x_squared,self.peaky)
                sum_xy=np.sum(xy)
                N=np.sum(self.peaky)
                N_1=N-1
                standev=sum_xy/N_1
                standev=(standev)**(1/2)
                self.standerr=standev/((N**(1/2)))
                self.x_mean_high=self.standerr
                
                
                       
                               
                if self.backSelec.isChecked()==True:
                    self.plt.addItem(self.regplot)
                    
         
                    
                    if self.logScale.isChecked()==True:
                    
                        color=pg.intColor(0, alpha=50)
                        brush=pg.mkBrush(color=color)
                        x1=self.x1range
                        
                        y=self.reg1yrange
                        y1=[]
                        
                        for i in range(len(y)):
                            if y[i]==0:
                                y1.append(.1)
                            else:
                                y1.append(y[i])
                        y1=np.log10(y1)     
                        
                        while len(x1)<=len(y1):
                            x1=np.append(x1,x1[-1]+1)
                        
                        x2=self.x2range
                        y=self.reg2yrange
                        y2=[]
                        for i in range(len(y)):
                            if y[i]==0:
                                y2.append(.1)
                            else:
                                y2.append(y[i])
                        y2=np.log10(y2)
                        
                        while len(x2)<=len(y2):
                            x2=np.append(x2,x2[-1]+1)
                        
                        self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                     
                        
                        
                    if self.logScale.isChecked()==False:
                        color=pg.intColor(0, alpha=50)
                        brush=pg.mkBrush(color=color)
                        x1=self.x1range
                        y1=self.reg1yrange
                        
                        while len(x1)<=len(y1):
                            x1=np.append(x1,x1[-1]+1)
                        
                        x2=self.x2range
                        y2=self.reg2yrange
                        
                        while len(x2)<=len(y2):
                            x2=np.append(x2,x2[-1]+1)
                        
                        self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        
                    self.plt.addItem(self.reg1fill)
                    self.plt.addItem(self.reg2fill)
                    self.plt.removeItem(self.backReg1)
                    self.plt.removeItem(self.backReg2)
                   
                    
                   
                    
                    x1_center=(self.x1range[-1]+self.x1range[0])/2
                    x2_center=(self.x2range[-1]+self.x2range[0])/2
                    
                    slope=(self.reg2avgy-self.reg1avgy)/(x2_center-x1_center)

                    poiss_bk=[]
                    back=[]
                    
                    for i in range(len(self.peakx)):
                        x_val=self.peakx[i]-x1_center
                        b=self.reg1avgy+(slope*x_val)
                        back.append(b)

                        
                   
                    regular_array=np.array(self.peaky)-np.array(back)
                    
       
                    

                    #Channel range of the selected peak
                    channelrange=self.xmax-self.xmin
                    
                    NetSum1=sum(regular_array)
                    
                    
                    unc1=(sum(self.peaky)+sum(back))**(1/2)
                    
                    
                    nonNegArray=[count if count>=0 else 0 for count in regular_array]
                    
                    peakCentroid1=np.multiply(self.peakx,nonNegArray)
                    peakCentroid1=np.sum(peakCentroid1)/np.sum(nonNegArray)
                    
         
                    
                    x_squared=(self.peakx-peakCentroid1)**2
                    
                    xy=np.multiply(x_squared,nonNegArray)
                    
                    sum_xy=np.sum(xy)
                    N=np.sum(nonNegArray)
                
                    N_1=N-1

                    standev=sum_xy/N_1
         
                    standev=(standev)**(1/2)

                    self.standerr1=standev/((N**(1/2)))
        
                    self.dataWidget.append("""<br> <u>FREQUENTIST ANALYSIS<u>""")

                    self.dataWidget.append("""Peak Channel Range= """+str(firstchannel)+" to " + str(lastchannel)+
"""
Signal Counts= """ +str(NetSum1)+ " +/- " + str(unc1) +
"""
Centroid= """ + str(peakCentroid1)+  " +/- " + str(self.standerr1))
                    self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                
                 

                if self.backSelec.isChecked()==False:
    #Uncertainity of the total count
                    unc=(totalsum)**(1/2)
                    
                   

                    self.dataWidget.append("""<br> <u>FREQUENTIST ANALYSIS<u>""")
                    self.dataWidget.append("""Peak Channel Range= """+str(firstchannel)+" to " + str(lastchannel)+
"""
Signal Counts= """ +str(totalsum)+ " +/- " + str(unc)+
"""
Centroid= """+str(self.x_mean)+" +/- " + str(self.standerr))
                    self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                self.peakSelect.setChecked(False)
                self.backSelec.setChecked(False)
                
     
                    
                
        if self.sumAction.isChecked()==False:
            names=[item.name() for item in self.plt.listDataItems()]
            
            
            if "reg1fill" in names:
                try:
                    
                    self.mcmcAction.setEnabled(True)
                    self.gaussFitAction.setEnabled(True)
                    self.plt.removeItem(self.totalfill)
                    self.peakReg.setRegion((self.xmin,self.xmax))
                    self.plt.addItem(self.peakReg)
                    self.peakSelect.setChecked(True)
                    
                    
                    self.plt.removeItem(self.reg1fill)
                    self.plt.removeItem(self.reg2fill)
                    self.plt.removeItem(self.regplot)
                    self.backReg1.setRegion((self.reg1xmin,self.reg1xmax))
                    self.backReg2.setRegion((self.reg2xmin,self.reg2xmax))
                    self.plt.addItem(self.backReg1)
                    self.plt.addItem(self.backReg2)
                    self.backSelec.setChecked(True)
            
                    
                    
                except:
                    pass
                
                try:
                     self.tabs.removeTab(1)
                     self.tabs.removeTab(1)
                     self.tabs.removeTab(1)
                     self.tabs.removeTab(1)
                except:
                    pass
                
            elif "totalFill" in names:
     
                self.plt.removeItem(self.totalfill)
                self.peakReg.setRegion((self.xmin,self.xmax))
                self.plt.addItem(self.peakReg)
                
    
                self.mcmcAction.setEnabled(True)
                self.gaussFitAction.setEnabled(True)
                self.peakSelect.setChecked(True)
                


            
    def RadioButtonClick(self):
        if self.b1.isChecked()==True:
            self.tnProb=True
            
            self.prob_x1.setEnabled(True)
            self.prob_x2.setEnabled(True)
            
        if self.b1.isChecked()==False:
            self.tnProb=False
            self.b1.setChecked(False)
            

            
        if self.b2.isChecked()==True:
            self.gProb=True
            
            self.prob_x1.setEnabled(True)
            self.prob_x2.setEnabled(True)
            
        if self.b2.isChecked()==False:
            self.gProb=False
            self.b2.setChecked(False)
            
        if self.tnProb==False and self.gProb==False:
            self.prob_x1.setEnabled(False)
            self.prob_x2.setEnabled(False)
         
            
         
            
         
    def MCMC(self):
        if self.mcmcAction.isChecked()==True:
            if self.backSelec.isChecked()==False:
                
                self.dataWidget.append(
"""
Select peak and background first!""")
                self.mcmcAction.setChecked(False)
                
            if self.backSelec.isChecked()==True:

                self.gaussFitAction.setEnabled(False)
                self.sumAction.setEnabled(False)
                    
                paraWidget=QDialog()
                
                sample_size = QLineEdit(paraWidget)
                burnin= QLineEdit(paraWidget)
                chain_numbers=QLineEdit(paraWidget)
                title=QLabel(paraWidget)
                self.prob_x1 = QLineEdit(paraWidget)
                self.prob_x2=QLineEdit(paraWidget)
                empty_string=QLabel(paraWidget)
                
                
                self.tnProb=False
                self.gProb=False
                
                self.prob_x1.setEnabled(False)
                self.prob_x2.setEnabled(False)
                
                
                
                self.buttonGroup = QtGui.QButtonGroup()
                
                
                self.b1=QRadioButton("")
                self.b2=QRadioButton("")
                
                
                self.buttonGroup.addButton(self.b1)
                self.buttonGroup.addButton(self.b2)
                
                self.buttonGroup.setExclusive(False)
                self.b1.toggled.connect(self.RadioButtonClick)
                self.b2.toggled.connect(self.RadioButtonClick)
                
  

        
                buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
                layout = QFormLayout(paraWidget)
                layout.addRow("Sample Size: ", sample_size)
                layout.addRow("Burn-in Size: ", burnin)
                layout.addRow("Number of Chains",chain_numbers)
                layout.addRow("",empty_string)
                layout.addRow("Calculate Probability of Signal Between:",title)
                layout.addRow("Value 1 ", self.prob_x1)
                layout.addRow("Value 2 ",self.prob_x2)
                layout.addRow("Trunc. Norm.",self.b1)
                layout.addRow("Gamma",self.b2)
                
    
                layout.addWidget(buttonBox)
                buttonBox.accepted.connect(paraWidget.accept)
                paraWidget.exec()
    
                
                
                #Creates a fillable region
                x=self.peakx
                y=self.peaky
                color=pg.mkColor(0,255,255,50)
                pen=pg.mkPen(color="k",width=2)
                brush=pg.mkBrush(color=color)
             
                self.totalfill= pg.PlotCurveItem(name="totalFill")
        
                if len(x)==len(y):
                    x=np.append(x,x[-1]+1)
                if self.logScale.isChecked()==True:
                    y=np.log10(y)
                self.totalfill.setData(x,y,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                   
        
                
                if self.logScale.isChecked()==True:
                        color=pg.intColor(0, alpha=50)
                        brush=pg.mkBrush(color=color)
                        x1=self.x1range
                        
                        y=self.reg1yrange
                        y1=[]
                        for i in range(len(y)):
                            if y[i]==0:
                                y1.append(.1)
                            else:
                                y1.append(y[i])
                        y1=np.log10(y1)     
                        
                        while len(x1)<=len(y1):
                            x1=np.append(x1,x1[-1]+1)
                        
                        x2=self.x2range
                        y=self.reg2yrange
                        y2=[]
                        for i in range(len(y)):
                            if y[i]==0:
                                y2.append(.1)
                            else:
                                y2.append(y[i])
                        y2=np.log10(y2)
                        
                        while len(x2)<=len(y2):
                            x2=np.append(x2,x2[-1]+1)
                        
                        self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                
                if self.logScale.isChecked()==False:
                        color=pg.intColor(0, alpha=50)
                        brush=pg.mkBrush(color=color)
                        x1=self.x1range
                        y1=self.reg1yrange
                        while len(x1)<=len(y1):
                            x1=np.append(x1,x1[-1]+1)
                        
                        x2=self.x2range
                        y2=self.reg2yrange
                        while len(x2)<=len(y2):
                            x2=np.append(x2,x2[-1]+1)
                        
                        self.reg1fill.setData(x1,y1,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        self.reg2fill.setData(x2,y2,pen=pen,fillLevel=0,brush=brush,stepMode=True)
                        
                #Gets the first and last channel of the selected region
                firstchannel=int(round(self.peakx[0]))
                lastchannel=int(round(self.peakx[-1]))
                

            
                    
                    
#Gets slope of the line created from the chosen background regions
                
                y1rang=self.reg1yrange
                
                            
                x1mean=np.sum(self.x1range)/len(self.x1range)
               
                
                y2rang=self.reg2yrange
          
                  
               
                
                x2mean=np.sum(self.x2range)/len(self.x2range)
               
                bkg_1=np.sum(y1rang)/len(y1rang)

 
                
                bkg_2=np.sum(y2rang)/len(y2rang)  
                   
                self.slope=float((bkg_2-bkg_1)/(x2mean-x1mean))
    
                
                
                
                
    
                
                background=[]
            
                for i in range(len(self.peakx)):
                    x_val=self.peakx[i]-x1mean
                    back=bkg_1+(self.slope*x_val)                                                    
                    background.append(back)
                    
                    
           

               
        #Channel range of the selected peak
                channelrange=self.xmax-self.xmin
        #Multiplies the average per channel by the number of channels of the peak
            

#Observed values array
                obs_tot=list(self.peaky)
      
                
                
#Having NaN values as background raises an error when running the Poisson
#This loop replaces any NaN values with zero
    
                obs_bkg=[]
                bkg_width=0
    
    
                for i in range(len(obs_tot)):
                
                    if np.isnan(background[i])==True:
                        obs_bkg.append(0)
                    else:
                        b=background[i]
                        obs_bkg.append(int(round(b)))
                        
                        bkg_width+=b
                        
                
                num=list(range(len(obs_tot)))
        
                
                tot_width=int(round(sum(obs_tot)))
   
                bkg_width=int(round(bkg_width))
                
                #Having zero as the total width raises an error
               
                if tot_width==0:
                    tot_width=1
                    print("Detected no counts in the peak region, added 1 count to avoid raising error in the algorithm")
                    
                if bkg_width==0:
                    print("Detected no counts in the background region, added 1 count to avoid raising error in the algorithm")
          
                    bkg_width=1
                if sample_size.text()=="" or sample_size.text()==0:
                    samples=3000
                else:
                    samples=int(sample_size.text())
                    
    
                        
                if burnin.text()=="" or burnin.text()==0:
                    tune=1000
                else:
                    tune=int(burnin.text())
                    
                        
                if chain_numbers.text()=='' or chain_numbers.text()==0:
                    chain_num=3
                else:
                    chain_num=int(chain_numbers.text())
                maxcount=int(np.amax(self.peaky))
                maxbkg=np.amax(obs_bkg)
                
                max_chan=max(self.peakx)

                peakXRange=self.peakx
                peakCounts=self.peaky
                backCounts=obs_bkg
        
         
                self.dataWidget.append(
"""
Running Bayesian MCMC...""")
                self.dataWidget.moveCursor(QtGui.QTextCursor.End) 
                
                
                #I accidentally wrote all of the preceeding code with an extra 
                #indentation and I didn't want to go through and correct it 
                #(out of laziness), thus the if True==True statement was born
                
                if True==True:
                    bayesianMCMCT="""
  function(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chainNum){
   
        library("rjags")
        library("HDInterval")
        load.module("glm")
 
xchann <- c(peakXRange)	

obstot <- tot_width


obsbkg<-bkg_width

 

tot_width<-tot_width
bkg_width<-bkg_width



cat('model {


obstot ~ dpois(s + xb)
obsbkg ~ dpois(xb)


# half-normal prior
# for the sigmas, we choose observed total and background counts 
 s ~ dnorm(0.0, pow(tot_width, -2))T(0,)
 xb ~ dnorm(0.0, pow(bkg_width, -2))T(0,)



}', file={f <- tempfile()})  



n.chains <- chainNum
n.adapt  <- tune
n.burn   <- tune 
n.iter   <- samples  
thin     <- 1


ourmodel <- jags.model(f, data = list(
			  obstot = obstot, 
			  obsbkg = obsbkg,
              tot_width=tot_width,
              bkg_width=bkg_width
			                     ),
               n.chains = n.chains, n.adapt = n.adapt, quiet=TRUE)
  
update(ourmodel, n.burn)

# variable.names are variables to be recorded in output file of samples
mcmcChain <- coda.samples(ourmodel, 
			  variable.names=c(
			       's', 'xb'
			                  ),
                   n.iter=n.iter)

# <---- rjags
######################################################################
samplesmat = as.matrix(mcmcChain)
HDI68 <- hdi(samplesmat[,1], credMass = 0.68)
HDI95 <-hdi(samplesmat[,1], credMass = 0.95)
return(list(samplesmat,HDI68, HDI95))
    }
"""


                    bayesianMCMCG="""
  function(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chainNum){
   
        library("rjags")
        library("HDInterval")
        load.module("glm")
 
xchann <- c(peakXRange)	


obstot2 <- c(peakCounts)


obsbkg2<-c(backCounts)
 



totalObserved2<-tot_width


totObsBkg2<-bkg_width

######################################################################                  
# JAGS MODEL
######################################################################                 
# rjags ----->
cat('model {

# half-normal prior
  
  

  totalObserved2~dpois(a+bkg)
  totObsBkg2~dpois(bkg)

  


  
  a ~ dgamma(0.5,.00001)
  bkg~dgamma(0.5,.00001)




}', file={f <- tempfile()})  



n.chains <- chainNum
n.adapt  <- tune   
n.burn   <- tune 
n.iter   <- samples  
thin     <- 1



ourmodel <- jags.model(f, data = list(
            totalObserved2=totalObserved2,
            totObsBkg2=totObsBkg2,
              tot_width=tot_width,
              bkg_width=bkg_width
              
							  ),n.chains = n.chains, n.adapt = n.adapt, quiet=TRUE)
  
update(ourmodel, n.burn)


mcmcChain <- coda.samples(ourmodel, 
			  variable.names=c(
			       'a','bkg'
			                  ),
                   n.iter=n.iter)
samplesmat = as.matrix(mcmcChain)
HDI68 <- hdi(samplesmat[,1], credMass = 0.68)
HDI95 <-hdi(samplesmat[,1], credMass = 0.95)
return(list(samplesmat,HDI68, HDI95))
    }
"""



                    bayesCentT="""
  function(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chainNum){
   
        library("rjags")
        load.module("glm")
 
xchann <- c(peakXRange)	


obstot <- c(peakCounts)


obsbkg<-c(backCounts)
 



tot_width<-tot_width


bkg_width<-bkg_width

######################################################################                  
# JAGS MODEL
######################################################################                 
# rjags ----->
cat('model {


for ( i in 1 : length(obstot) ) {
  obstot[i] ~ dpois(s[i] + xb[i])
  obsbkg[i] ~ dpois(xb[i])
}


for ( i in 1 : length(obstot) ) {


  # half-normal prior
  s[i] ~ dnorm(0.0, pow(tot_width, -2))T(0,)
  xb[i] ~ dnorm(0.0, pow(bkg_width, -2))T(0,)
}

}', file={f <- tempfile()})  



n.chains <- chainNum
n.adapt  <- tune   
n.burn   <- tune 
n.iter   <- samples  
thin     <- 1

# "f": is the model specification from above; 
# data = list(...): define all data elements that are referenced in the 
# JAGS model

ourmodel <- jags.model(f, data = list(
			  obstot = obstot, 
			  obsbkg = obsbkg,
              tot_width=tot_width,
              bkg_width=bkg_width
							  ),
               n.chains = n.chains, n.adapt = n.adapt, quiet=TRUE)
  
update(ourmodel, n.burn)

# variable.names are variables to be recorded in output file of samples
mcmcChain <- coda.samples(ourmodel, 
			  variable.names=c(
			       's', 'xb'
			                  ),
                   n.iter=n.iter, thin)


centvec <- vector()
signalsum <- vector()

samplesmat <- as.matrix(mcmcChain)
# extract signal sum 
signalsum <- rowSums(samplesmat[, 1 : length(obstot)])
# extract signals for individual channels
signalmat <- samplesmat[, 1 : length(obstot)]

# compute centroid by matrix multiplication: row x column
centvec <- (signalmat%*%xchann)/signalsum

return(centvec)
    }
"""
       



                    bayesCentG="""
  function(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chainNum){
   
        library("rjags")
        load.module("glm")
 
xchann <- c(peakXRange)	


obstot <- c(peakCounts)


obsbkg<-c(backCounts)
 



######################################################################                  
# JAGS MODEL
######################################################################                 
# rjags ----->
cat('model {


for ( i in 1 : length(obstot) ) {
  obstot[i] ~ dpois(s[i] + xb[i])
  obsbkg[i] ~ dpois(xb[i])
}


for ( i in 1 : length(obstot) ) {


  # half-normal prior
  s[i] ~ dgamma(0.5, .00001)
  xb[i] ~ dnorm(0.5,.000005)
}

}', file={f <- tempfile()})  



n.chains <- chainNum
n.adapt  <- tune   
n.burn   <- tune 
n.iter   <- samples  
thin     <- 1

# "f": is the model specification from above; 
# data = list(...): define all data elements that are referenced in the 
# JAGS model

ourmodel <- jags.model(f, data = list(
			  obstot = obstot, 
			  obsbkg = obsbkg
							  ),
               n.chains = n.chains, n.adapt = n.adapt, quiet=TRUE)
  
update(ourmodel, n.burn)

# variable.names are variables to be recorded in output file of samples
mcmcChain <- coda.samples(ourmodel, 
			  variable.names=c(
			       's', 'xb'
			                  ),
                   n.iter=n.iter, thin)


centvec <- vector()
signalsum <- vector()

samplesmat <- as.matrix(mcmcChain)
# extract signal sum 
signalsum <- rowSums(samplesmat[, 1 : length(obstot)])
# extract signals for individual channels
signalmat <- samplesmat[, 1 : length(obstot)]

# compute centroid by matrix multiplication: row x column
centvec <- (signalmat%*%xchann)/signalsum

return(centvec)
    }
"""
                    

                    bayesTrunc=robjects.r(bayesianMCMCT)
                    truncNormResults=bayesTrunc(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chain_num)
        
                    ##HDI is calculated according to 68
                    truncNormHDI68=[truncNormResults[1][0],truncNormResults[1][1]]
                    
                    ##Second HDI is according to 95 credible mass region
                    truncNormHDI95=[truncNormResults[2][0],truncNormResults[2][1]]
                    
                    trace1=np.transpose(np.array(truncNormResults[0]))
                    trace1=trace1[0]
                    
                    
                
                    
                    bayesGam=robjects.r(bayesianMCMCG)
                    gamResults=bayesGam(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chain_num)
                    
                    ##HDI is calculated according to 68
                    gamHDI68=[gamResults[1][0],gamResults[1][1]]
                    
                    ##Second HDI is according to 95 credible mass region
                    gamHDI95=[gamResults[2][0],gamResults[2][1]]
                    
                    trace2=np.transpose(np.array(gamResults[0]))
                    trace2=trace2[0]
                    
                    
                    bayesTCent=robjects.r(bayesCentT)
                    trace3=np.array(bayesTCent(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chain_num))
                    trace3=np.transpose(trace3)
                    trace3=trace3[0]
                  
                  
                    
                    bayesGCent=robjects.r(bayesCentG)
                    trace4=np.array(bayesGCent(peakXRange,peakCounts,backCounts,tot_width,bkg_width,samples,tune,chain_num))
                    trace4=np.transpose(trace4)
                    trace4=trace4[0]
                
                    
                    trace=[trace1,trace2]
                    
                 
                        
                    
                    trace=np.array(trace)
                
                
                    thin=int(len(trace[0])/2000)
                    if thin==0:
                        thin=1
                    
                    
    #Arrays that store  the data from each step of the algorthm
                    num=len(trace[0])
    
                    t_totarray=[]
                    t_bkgarray=[]
                    
                    g_totarray=[]
                    g_bkgarray=[]
                   
                    tchains=[]
                    gchains=[]
                    

                    
            
#Puts the arrays containing the total peak sum of the entries at each step into two seperate lists
             
                
                tn_s=trace[0]
                g_s=trace[1]
                

                    
                self.tn_s=tn_s
                self.g_s=g_s
            
#Returns the quartiles of both list
                pertot=np.percentile(tn_s,[2.5,16,50,84,97.4])

                
                g_pertot=np.percentile(g_s,[2.5,16,50,84,97.4])
                
     
    
    #Takes a 64% error by subtracting the 84% and 16% quartiles from the median 
                Median_S=float(pertot[2])
                x_2=float(pertot[0])
                x_16=float(pertot[1])
                x_50=float(pertot[2])
                x_84=float(pertot[3])
                x_97=float(pertot[4])
                Upper_Bound=float(pertot[3]-pertot[2])
                
     
                Lower_Bound=float(pertot[2]-pertot[1])

                
                g_Median_S=float(g_pertot[2])
                g_x_2=float(g_pertot[0])
                g_x_16=float(g_pertot[1])
                g_x_50=float(g_pertot[2])
                g_x_84=float(g_pertot[3])
                g_x_97=float(g_pertot[4])
                g_Upper_Bound=float(g_pertot[3]-g_pertot[2])
                
               
                g_Lower_Bound=float(g_pertot[2]-g_pertot[1])
                
   
    
                
                t_totsum=np.array(trace1)
                g_totsum=np.array(trace2)
 
                colors=["b","r","g","c","m","y","k"]
               
                for i in range(chain_num):
                    if i>=len(colors):
                        colors.append(colors[i-7])
                    if i==len(colors):
                        colors.append("b")
                    if i==(chain_num)-1:
                        colors.append(colors[i-6])
                
                chainplt=pg.PlotWidget()
                chainplt.addLegend()
                
                if self.fileName=="testing":
                    file=open("test_data_storage.dat")
                    self.test_values=file.readlines()
                    file.close
                    true_count=self.test_values[0].strip().split()
                    true_count=int(true_count[3])
                    
                    actual_count=self.test_values[-6].strip().split()
                    actual_count=int(float(actual_count[3]))

                    
                    pen1=pg.mkPen("r",width=3)
                    pen2=pg.mkPen("r",width=3,style=QtCore.Qt.DashLine)
                    true_mean_line=chainplt.plot(x=true_count,pen=pen1,name="True Mean")
                    actual_mean_line=chainplt.plot(x=actual_count,pen=pen2,name="Actual Mean")
                    chainplt.addLine(x=true_count,pen=pen1)
                    chainplt.addLine(x=actual_count,pen=pen2)
                    
                
                t_s_chains=[]
                g_s_chains=[]
                
                for i in range(chain_num):
                    start=int(round(i*len(trace[0])/chain_num))
                    stop=int(round((i+1)*len(trace[0])/chain_num))
                    
                    if i==chain_num-1:
                         stop=int(round((i+1)*len(trace[0])/chain_num))-1
                    
                    t_chain=trace[0][start:stop]
                    t_s_chains.append([t_chain])
                   
                    g_chain=trace[1][start:stop]
                    g_s_chains.append([g_chain])
              
                for i in range(chain_num):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(t_s_chains[i][0]),np.amax(t_s_chains[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(t_s_chains[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[i],width=2)
                    
                    #Plots the smoothed curve 
                    chainplt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Trunc. Norm.)")
                
                
                for i in range(chain_num):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(g_s_chains[i][0]),np.amax(g_s_chains[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(g_s_chains[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[6-i],width=2)
                    
                    #Plots the smoothed curve 
                    chainplt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Gamma)")
                chainplt.setMouseEnabled(x=False,y=False)
                
                
                
                netCountHist=pg.PlotWidget()
                netCountHist.addLegend()
                
            
                    
                
                tnCountHist=[]
                gCountHist=[]
                
                for i in range(len(tn_s)):
                    tnCountHist.append(int(round(tn_s[i])))
                    gCountHist.append(int(round(g_s[i])))
                    
                tnBins=list(range(min(tnCountHist),max(tnCountHist)+1))
                gBins=list(range(min(gCountHist),max(gCountHist)+1))
                
                
                
                tnY=sp.stats.gaussian_kde(tnCountHist)(tnBins)
                gY=sp.stats.gaussian_kde(gCountHist)(gBins)
                   
                file=open("Trunc_Norm_Pos.dat","w+")
            
                for i in range(len(tnBins)):
                    file.write("{0}\t{1}\n".format(tnBins[i],tnY[i]))
                
                file.close()
            
                file=open("Gamma_Pos.dat","w+")
                
                for i in range(len(gBins)):
                    file.write("{0}\t{1}\n".format(gBins[i],gY[i]))
                file.close()
            

                
                
                s_traces=pg.PlotWidget()
                
                s_traces.addLegend()
                
       
                
                for i in range(chain_num):
                    x=range(0,len(t_s_chains[0][0]),thin)
                    y=t_s_chains[i][0]
                    y=y[::thin]
                    
                    if len(x)>len(y):
                        x=x[0:-1]

                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    s_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Trunc. Norm.)")
                    
                for i in range(chain_num):
                    x=range(0,len(g_s_chains[0][0]),thin)
                    y=g_s_chains[i][0]
                    y=y[::thin]
                    
                    if len(x)>len(y):
                        x=x[0:-1]
                    
                    color=pg.intColor(2*i, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    s_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Gamma)")
                    
                s_traces.setMouseEnabled(x=False,y=False)
                    

                self.tab2=chainplt
                self.tabs.addTab(self.tab2,"Signal Counts Posterior")
                
            
                self.tab3=s_traces
                self.tabs.addTab(self.tab3,"Traces Net Counts")
                
#Gets the mean channel by taking the mean per step, summing these and placing
#the values in a list        

                
            
        
          
                x1_mean=list(trace3)
                
               
                x2_mean=list(trace4)
                
                tCentArray=x1_mean
                gCentArray=x2_mean
                
                t_x_mean_quart=np.percentile(x1_mean,[16,50,84])
                t_x_median=t_x_mean_quart[1]
                t_upper=t_x_mean_quart[2]-t_x_median
                t_lower=t_x_median-t_x_mean_quart[0]
                
                g_x_mean_quart=np.percentile(x2_mean,[16,50,84])
                g_x_median=g_x_mean_quart[1]
                g_upper=g_x_mean_quart[2]-g_x_median
                g_lower=g_x_median-g_x_mean_quart[0]
    
        


                
                
                
                centplt=pg.PlotWidget()
                centplt.addLegend()
                
                if self.fileName=="testing":
        
                    true_centroid=self.test_values[2].strip().split()
                    true_centroid=float(true_centroid[3])
                    
                    actual_centroid=self.test_values[-4].strip().split()
                    actual_centroid=float(actual_centroid[2])
                    
                    
                    pen1=pg.mkPen("r",width=3)
                    pen2=pg.mkPen("r",width=3,style=QtCore.Qt.DashLine)
                    
                    true_centroid_line=centplt.plot(x=true_centroid,y=None,pen=pen1,name="True Centroid" )
                    actual_centroid_line=centplt.plot(x=actual_centroid,y=None,pen=pen2,name="Actual Centroid")
                    centplt.addLine(x=true_centroid,y=None,pen=pen1)
                    centplt.addLine(x=actual_centroid,y=None,pen=pen2)
     
            
 
                    
                    
       

                
                for i in range(chain_num):
                    start=int(round(i*len(trace3)/chain_num))
                    stop=int(round((i+1)*len(trace3)/chain_num))
                    
            
                    
                    if i==chain_num-1:
                         stop=int(round((i+1)*len(trace1)/chain_num))-1
                    
                    t_chain=trace3[start:stop]
                    t_chain=list(t_chain)
                
        
            
                    chain_centroid=t_chain
                    y_sm=np.array(chain_centroid)
                    chanmin,chanmax=np.amin(chain_centroid),np.amax(chain_centroid)
                    x_smooth = np.linspace(chanmin, chanmax, 200)
                    y_smooth = sp.stats.gaussian_kde(y_sm)(x_smooth)
                    pen=pg.mkPen(color=colors[i],width=2)
                    centplt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Trunc. Norm.)")
                    
                for i in range(chain_num):
                    
                    
                    start=int(round(i*len(trace1)/chain_num))
                    stop=int(round((i+1)*len(trace1)/chain_num))
                    
                    if i==chain_num-1:
                         stop=int(round((i+1)*len(trace1)/chain_num))-1
                
                
                   
                    g_chain=trace4[start:stop]
                    g_chain=list(g_chain)
                    
                    
                    
                    chain_centroid=list(g_chain)
                    y_sm=np.array(chain_centroid)
                    chanmin,chanmax=np.amin(chain_centroid),np.amax(chain_centroid)
                    x_smooth = np.linspace(chanmin, chanmax, 200)
                    y_smooth = sp.stats.gaussian_kde(y_sm)(x_smooth)
                    pen=pg.mkPen(color=colors[6-i],width=2)
                    centplt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Gamma)")
                    
                    
                centplt.setMouseEnabled(x=False,y=False) 
                self.tab4=centplt
                self.tabs.addTab(self.tab4,"Centroid Posterior")
                
                

                
                centHist=[]
            
                
                for i in range(len(tCentArray)):
                    centHist.append(round(tCentArray[i],2))       
                    
                X=np.arange(min(centHist),max(centHist)+.01,.01)
                centX=[round(num,2) for num in X]
                
                centY=[]
                
                for i in range(len(centX)):
                    centY.append(centHist.count(centX[i]))

  
                
                while len(centX)<len(centY)+1:
                    centX.append(centX[-1]+.01)
                    
                
                
                cent_traces=pg.PlotWidget()
                cent_traces.addLegend()
                
                for i in range(chain_num):
                    start=int(round(i*len(trace3)/chain_num))
                    stop=int(round((i+1)*len(trace3)/chain_num))
                    
            
                    
                    if i==chain_num-1:
                         stop=int(round((i+1)*len(trace1)/chain_num))-1
                    
                    t_chain=trace3[start:stop]
                    t_chain=list(t_chain)
                    
                    
                    x=range(0,len(t_chain),thin)
                    y=t_chain
                    y=y[::thin]
        
                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    cent_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Trunc. Norm.)")
                    
                for i in range(chain_num):
                    
                    
                    start=int(round(i*len(trace3)/chain_num))
                    stop=int(round((i+1)*len(trace3)/chain_num))
                    
            
                    
                    if i==chain_num-1:
                         stop=int(round((i+1)*len(trace1)/chain_num))-1
                    
                    g_chain=trace4[start:stop]
                    g_chain=list(g_chain)
                    
                    
                    x=range(0,len(g_chain),thin)
                    y=g_chain
                    y=y[::thin]
                    color=pg.intColor(2*i, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    cent_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1)+" (Gamma)")
                    
                
                cent_traces.setMouseEnabled(x=False,y=False)
                
                
                self.plt.addItem(self.reg1fill)
                self.plt.addItem(self.reg2fill)
                self.plt.addItem(self.regplot)
                self.plt.addItem(self.totalfill)
                
                self.plt.removeItem(self.backReg1)
                self.plt.removeItem(self.backReg2)
                self.plt.removeItem(self.peakReg)
                
                
                self.tab5=cent_traces
                self.tabs.addTab(self.tab5,"Traces Centroid")
                    
                self.peakSelect.setChecked(False)
                self.backSelec.setChecked(False)
                
      
                
                
                self.dataWidget.append("""
                                       
<br> <u>BAYESIAN ANALYSIS<u>""")
               
                self.dataWidget.append("""Parameters: Sample Size= """+str(samples)+"\t Burn= "+str(tune)+"    Chains= "+str(chain_num)+

"""
Peak Channel Range: """+str(firstchannel)+" to " + str(lastchannel))
                self.dataWidget.append("""<b>Truncated Normal Posterior<b>""")
                self.dataWidget.append("""Signal Counts: """ +str(Median_S)+ " + "+ str(Upper_Bound)+ "/- "+str(Lower_Bound) +
"""
Centroid: """ + str(t_x_median)+  " + "  + str(t_upper)+"/- " + str(t_lower)+
"""
Signal Count HDI (68%): """+str(truncNormHDI68[0])+" - "+str(truncNormHDI68[1])+
"""
Signal Count HDI (95%): """+str(truncNormHDI95[0])+" - "+str(truncNormHDI95[1])+
"""
Signal Counts Percentiles: """+
"""
2.5%= """+str(x_2)+ "   16%= "+str(x_16)+"   50%= "+str(x_50)+"   84%= "+str(x_84)+"   97.5%= "+str(x_97))
                self.dataWidget.append("""<b>Gamma Posterior<b>""")
                self.dataWidget.append("""Signal Counts: """ +str(g_Median_S)+ " + "+ str(g_Upper_Bound)+ "/- "+str(g_Lower_Bound) +

"""
Centroid: """ + str(g_x_median)+  " + "  + str(g_upper)+"/- " + str(g_lower)+
"""
Signal Count HDI (68%): """+str(gamHDI68[0])+" - "+str(gamHDI68[1])+
"""
Signal Count HDI (95%): """+str(gamHDI95[0])+" - "+str(gamHDI95[1])+
"""
Signal Counts Percentiles: """+
"""
2.5%= """+str(g_x_2)+ "   16%= "+str(g_x_16)+"   50%= "+str(g_x_50)+"   84%= "+str(g_x_84)+"   97.5%= "+str(g_x_97))

                self.dataWidget.moveCursor(QtGui.QTextCursor.End)





                
                ######Runs the probability function below 
                
                if self.tnProb==True:
                    self.tnProb=False
                    try:
                        minChan=int(self.prob_x1.text())
                        maxChan=int(self.prob_x2.text())
                        data=self.tn_s
                        Spectrum.Prob(self,[minChan,maxChan],data,"Truncated Normal")
                    except:
                        self.dataWidget.append("Invalid channel region chosen for probability calculation")
                        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                if self.gProb==True:
                    self.gProb=False
                    try:
                        minChan=int(self.prob_x1.text())
                        maxChan=int(self.prob_x2.text())
                        data=self.g_s
                        Spectrum.Prob(self,[minChan,maxChan],data,"Gamma")
                    except:
                        self.dataWidget.append("Invalid channel region chosen for probability calculatio")
                        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
                        
    
                        
                        
                        

        if self.mcmcAction.isChecked()==False:
            names=[item.name() for item in self.plt.listDataItems()]
               
            if "reg1fill" in names:
                    
              
                self.peakReg.setRegion((self.xmin,self.xmax))
                self.plt.removeItem(self.totalfill)  
                self.plt.addItem(self.peakReg)
            

                self.gaussFitAction.setEnabled(True)
                self.sumAction.setEnabled(True)
   
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                self.tabs.removeTab(1)
                     
                self.peakSelect.setChecked(True)
                self.plt.removeItem(self.reg1fill)
                self.plt.removeItem(self.reg2fill)
                self.plt.removeItem(self.regplot)
                self.backReg1.setRegion((self.reg1xmin,self.reg1xmax))
                self.backReg2.setRegion((self.reg2xmin,self.reg2xmax))
                self.plt.addItem(self.backReg1)
                self.plt.addItem(self.backReg2)
                self.backSelec.setChecked(True)
                
                self.backUsed=0
                
       
                
            
             
    
    def Prob(self,channelRange,data,summationType):
        
    
                
        x1=float(channelRange[0])
        x2=float(channelRange[-1])
                
        per1=0
                
        vals1=data
        vals2=data
        
        prob1=np.percentile(vals1,[per1])
        while prob1<x1:
            per1+=.05
            prob1=np.percentile(vals1,[per1])
        
        if per1==0:
            probability1=0
        elif abs(np.percentile(vals1,[per1-.05])-x1)>abs(x1-prob1):
            probability1=round(per1,2)
        else:
            probability1=round(per1-.05,2)
                    
                    
        per2=0
        prob2=np.percentile(vals2,[per2])
        while prob2<x2:
            per2+=.05
            prob2=np.percentile(vals2,[per2])
        
        if per2==0:
            probability2=0
        elif abs(np.percentile(vals2,[per2-.05])-x2)>abs(x2-prob2):
            probability2=round(per2,2)
        else:
            probability2=round(per2-.05,2)
                    
        probability=round(abs(probability2-probability1),2)
           
        summationType=summationType
               
        self.dataWidget.append("""

Probability of the signal being between """+str(x1)+" and "+str(x2)+ " counts is "+str(probability)+"% ("+str(summationType)+")")
                

        self.dataWidget.moveCursor(QtGui.QTextCursor.End)    
                
        
        
                    
        

        
       
    def GaussFit(self):
        if self.gaussFitAction.isChecked()==True:
            
            if self.backSelec.isChecked()==False:
                self.dataWidget.append(
"""
Select peak and background first!""")
                self.gaussFitAction.setChecked(False)
                self.dataWidget.moveCursor(QtGui.QTextCursor.End) 
            
            
            if self.backSelec.isChecked()==True:
                
                
                
    
                self.mcmcAction.setEnabled(False)
                self.sumAction.setEnabled(False)
                
                
                self.sigmaS=False
                self.sigmaP=False
                
                
                self.fitWidget=QDialog()
                self.staticSigma=QRadioButton("")
                self.paramSigma=QRadioButton("")
                
                self.sigma=QLineEdit(self.fitWidget)
                self.mu=QLineEdit(self.fitWidget)
                
                self.paramSigma.toggled.connect(self.fitRadioButtonClick)
                self.paramSigma.setChecked(True)
                
                self.staticSigma.toggled.connect(self.fitRadioButtonClick)
                self.staticSigma.setChecked(False)
                
                
                sampleSize=QLineEdit(self.fitWidget)
                burn=QLineEdit(self.fitWidget)
                chains=QLineEdit(self.fitWidget)
                self.sigma.setEnabled(False)
                self.mu.setEnabled(False)
                
                
                self.gaussProb_x1 = QLineEdit(self.fitWidget)
                self.gaussProb_x2=QLineEdit(self.fitWidget)
                empty_string=QLabel(self.fitWidget)
                title=QLabel(self.fitWidget)
                
                
                
                buttonBox= QDialogButtonBox(QDialogButtonBox.Ok, self)
                layout= QFormLayout(self.fitWidget)
                layout.addRow("Sample size: ", sampleSize)
                layout.addRow("Burn-in: ", burn)
                layout.addRow("Chains: ",chains)
                layout.addRow("Non-informative sigma",self.paramSigma)
                layout.addRow("Informative sigma",self.staticSigma)
                layout.addRow("Peak Standard Deviation: ",self.mu)
                layout.addRow("Error: ",self.sigma)
                layout.addRow("",empty_string)
                layout.addRow("Calculate Probability of Signal Between:",title)
                layout.addRow("Value 1: ",self.gaussProb_x1)
                layout.addRow("Value 2: ",self.gaussProb_x2)
                
                layout.addWidget(buttonBox)
                buttonBox.accepted.connect(self.fitWidget.accept)

    
                self.fitWidget.exec()
                
                if sampleSize.text()=="":
                    samples=2000
                if sampleSize.text()!="":
                    samples=int(sampleSize.text())
                if burn.text()=="":
                    tune=1500
                if burn.text()!="":
                    tune=int(burn.text())
                if chains.text()=="":
                    chainNum=2
                if chains.text()!="":
                    chainNum=int(chains.text())
                
            
                max_chan=max(self.peakx)

                peakXRange=self.peakx
                peakCounts=np.array([count if count>0 else 1 for count in self.peaky])
                back1Chans=self.x1range
                back1Counts=np.array([count if count>0 else 1 for count in self.reg1yrange])
                back2Chans=self.x2range
                back2Counts=np.array([count if count>0 else 1 for count in self.reg2yrange])
                firstChan=self.peakx[0]
                lastChan=self.peakx[-1]
                if self.sigmaS==True:
                    mean=float(self.mu.text())
                    std=float(self.sigma.text())
                    wEst=mean
              
                    
                if self.sigmaP==True:
                    mean=0
                    std=1000
                    wEst=(self.peakx[-1]-self.peakx[0])
                    
                    
                self.dataWidget.append(
"""
Running Gaussian Fitting MCMC...""")
                self.dataWidget.moveCursor(QtGui.QTextCursor.End) 
                
                
        
                r_string="""
  function(peakXRange,wEst,peakCounts,back1Chans,back1Counts,back2Chans,back2Counts,mean,std,samples,tune,chainNum,firstChan,lastChan){
   
        library("rjags")
        load.module("glm")
 
xchann <- c(peakXRange)	

obstot <- c(peakCounts)

mean <- mean

std<- std


 
xchann1 <- c(back1Chans)	

obsbkg1 <- c(back1Counts)


# data for right background region

xchann2 <- c(back2Chans)	

obsbkg2 <- c(back2Counts)

firstChan<-firstChan
lastChan<-lastChan


widthEst<-wEst
heightEst<-median(obstot)
centEst<-mean(xchann)
slopeEst<-mean(obsbkg2)-mean(obsbkg1)/(mean(xchann2)-mean(xchann1))


yIntEst<-obstot[0]

        

######################################################################                  
# JAGS MODEL
######################################################################                 
# rjags ----->
cat('model {



for ( i in 1 : length(xchann1) ) {
  obsbkg1[i] ~ dpois(zbkg1[i])  
# background linear model
  zbkg1[i] <- d * xchann1[i] + e
}

# left background region
for ( i in 1 : length(xchann2) ) {
  obsbkg2[i] ~ dpois(zbkg2[i])  
# background linear model
  zbkg2[i] <- d * xchann2[i] + e
}

# peak region
for ( i in 1 : length(xchann) ) {
  obstot[i] ~ dpois(zsig[i] + zbkg[i])

  zsig[i] <- a * exp( - ((xchann[i] - b)^2) /(2 * c^2) ) 
# background linear model
  zbkg[i] <- d* xchann[i] + e
}

######################################
#
# PRIORS
#
######################################




# half-normal prior
  a ~ dnorm(0.0, pow(1000, -2))T(0,)
  b ~ dunif(firstChan,lastChan)
  c ~dnorm(mean,pow(std,-2))T(0,)
  d ~ dnorm(0.0, pow(1000, -2))
  e ~ dnorm(0.0, pow(1000, -2))T(0,)

}', file={f <- tempfile()})  



n.chains <- chainNum
n.adapt  <- tune   
n.burn   <- tune 
n.iter   <- samples  
thin     <- 1



ourmodel <- jags.model(f, data = list(
                  xchann = xchann,
                 xchann1 = xchann1,
                 xchann2 = xchann2,
			   obstot = obstot, 
			  obsbkg1 = obsbkg1,
			  obsbkg2 = obsbkg2,
              mean=mean,
              std=std,
              firstChan=firstChan,
              lastChan=lastChan
							  ),

               inits = list(a = heightEst, b = centEst, c =widthEst , d = slopeEst,e=yIntEst),
               n.chains = n.chains, n.adapt = n.adapt, quiet=TRUE)
  
update(ourmodel, n.burn)


mcmcChain <- coda.samples(ourmodel, 
			  variable.names=c(
			       'a', 'b', 'c', 'd','e'
			                  ),
                   n.iter=n.iter, thin)
samplesmat = as.matrix(mcmcChain)

return(samplesmat)
    }
"""
    
    
       
                
       
                
                rfunc=robjects.r(r_string)
                trace=np.array(rfunc(peakXRange,wEst,peakCounts,back1Chans,back1Counts,back2Chans,back2Counts,mean,std,samples,tune,chainNum,firstChan,lastChan))
				
            
                
                trace=np.transpose(trace) 
                
                heights=np.array(trace[0])
                cents=np.array(trace[1])
                widths=np.array(trace[2])
                                              
                
                centPers=np.percentile(cents,[2.5,16,50,84,97.4])
                                                                  
                
                const=((2*np.pi)**(1/2))
                sigCounts=const*heights*widths
                sigPers=np.percentile(sigCounts,[2.5,16,50,84,97.4])
                
                heightPers=np.percentile(heights,[2.5,16,50,84,97.4])
                sigmaVals=np.percentile(widths,[2.5,16,50,84,97.4])
                
                centroid=centPers[2]
                upperC=centPers[3]-centroid
                lowerC=centroid-centPers[1]
                
         
       
                self.dataWidget.append("""<br> <u>GAUSSIAN FIT<u>""")
                
                self.dataWidget.append("""Parameters: Sample Size= """+str(samples)+"\t Burn= "+str(tune)+"     Chains= "+str(chainNum)+
"""
Peak Channel Range= """+str(int(self.peakx[0]))+" to " + str(int(self.peakx[-1]) )+
"""
Height= """+str(heightPers[2])+" + "+str(heightPers[3]-heightPers[2])+"/- "+str(heightPers[2]-heightPers[1])+
"""
Sigma= """+str(sigmaVals[2])+" + "+str(sigmaVals[3]-sigmaVals[2])+"/- "+str(sigmaVals[2]-sigmaVals[1])+
"""
Centroid= """+str(centroid)+" + "+str(upperC)+"/- "+str(lowerC)+
"""
Signal Counts= """+str(sigPers[2])+" + "+str(sigPers[3]-sigPers[2])+"/- "+str(sigPers[2]-sigPers[1]))
                
                self.dataWidget.moveCursor(QtGui.QTextCursor.End)                       
   
                ##Reduces the number of traces drawn for performance 
                #enhancing reasons 
                thin=int(len(trace[0])/2500)
            
                gaussThin=int(len(trace[0])/1000)
               
                
            #When log scale is on, it takes tremendously longer to generate the 
            #Gaussian plots for some reason
            
                if self.logScale.isChecked()==True:
                    thin=int(len(trace[0])/100)
                
                
                if thin==0:
                    thin=1
                if gaussThin==0:
                    gaussThin=1
                for i in range(0,len(trace[0]),gaussThin):
                    height=trace[0][i]
                    cent=trace[1][i]
  
                   
      

                    width=float(trace[2][i])
                    x_vals = np.linspace(int(self.x1range[0]), int(self.x2range[-1])+1, int(self.x2range[-1]-self.x1range[0]))
            
                    y_vals=[]
                    
                    
                    y=height * np.exp(-((x_vals - cent)**2 / (2 * width**2)))
                
                    #Calculates the linear background for that particular iteration
                    #based on the posterior 
                    
                    background=trace[3][i]*x_vals+trace[4][i]
                
                    #Adds this background to each y value
                    y_vals=y+background
                    
                
              
                    pen=pg.mkPen(color="r",width=1.5)
                    
                    self.plt.plot(x_vals,y_vals,pen=pen,name="gaussFit")
                    
                    colors=["b","r","g","c","m","y","k"]
          
               
                regXRange=list(range(int(round(self.x1range[0])),int(round(self.x2range[-1]))+1))
                regYRange=self.y[int(regXRange[0]-self.x[0]):int(regXRange[-1]-self.x[0])+1]
               
                regXRange.append(regXRange[-1]+1)
                regXRange=np.array(regXRange)
                highlightPen=pg.mkPen(color="b",width=2,alpha=100)
               
               
                self.plt.plot(regXRange,regYRange,pen=highlightPen,stepMode=True,name="regionHighlight")
               
                
               
                for i in range(chainNum):
                    if i>=len(colors):
                        colors.append(colors[i-7])
                    if i==len(colors):
                        colors.append("b")
                    if i==(chainNum)-1:
                            colors.append(colors[i-6])
                
                signalPos=pg.PlotWidget()
                signalPos.addLegend()
                    
             
                sigVals=[]
                for i in range(chainNum):
                    start=int(round(i*len(sigCounts)/chainNum))
                    stop=int(round((i+1)*len(sigCounts)/chainNum))
                    
                    if i==chainNum-1:
                         stop=int(round((i+1)*len(sigCounts)/chainNum))-1
                    
                    sig_val=sigCounts[start:stop]
                   
                    sigVals.append([sig_val])

                    
                for i in range(chainNum):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(sigVals[i][0]),np.amax(sigVals[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(sigVals[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[i],width=2)
                    
                    #Plots the smoothed curve 
                    signalPos.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.signalPosTab=signalPos
                signalPos.setMouseEnabled(x=False,y=False)
                        
                self.tabs.addTab(self.signalPosTab,"Signal Count Posterior")
                     
                
                signal_traces=pg.PlotWidget()
                signal_traces.addLegend()
                signal_traces.setMouseEnabled(x=False,y=False)
                
             
                
                for i in range(chainNum):
                    x=range(0,len(sigVals[0][0]),thin)
                    y=sigVals[i][0]
                    y=y[::thin]

                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    signal_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.sigTraceTab=signal_traces
                self.tabs.addTab(self.sigTraceTab,"Signal Count Traces")    
                
                
                
                
                
                
                
                
                
                aPos=pg.PlotWidget()
                aPos.addLegend()
                    
             
                aVals=[]
                for i in range(chainNum):
                    start=int(round(i*len(trace[0])/chainNum))
                    stop=int(round((i+1)*len(trace[0])/chainNum))
                    
                    if i==chainNum-1:
                         stop=int(round((i+1)*len(trace[0])/chainNum))-1
                    
                    a_val=trace[0][start:stop]
                   
                    aVals.append([a_val])

                    
                for i in range(chainNum):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(aVals[i][0]),np.amax(aVals[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(aVals[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[i],width=2)
                    
                    #Plots the smoothed curve 
                    aPos.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.aPosTab=aPos
                aPos.setMouseEnabled(x=False,y=False)
                        
                self.tabs.addTab(self.aPosTab,"Gaussian Height Posterior")
                     
                
                a_traces=pg.PlotWidget()
                a_traces.addLegend()
                a_traces.setMouseEnabled(x=False,y=False)
                
             
                
                for i in range(chainNum):
                    x=range(0,len(aVals[0][0]),thin)
                    y=aVals[i][0]
                    y=y[::thin]

                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    a_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.aTraceTab=a_traces
                self.tabs.addTab(self.aTraceTab,"Gaussian Height Traces")
                
                bPosPlt=pg.PlotWidget()
                bPosPlt.addLegend
                bPosPlt.setMouseEnabled(x=False,y=False)
                
                bVals=[]
                for i in range(chainNum):
                    start=int(round(i*len(trace[1])/chainNum))
                    stop=int(round((i+1)*len(trace[1])/chainNum))
                    
                    if i==chainNum-1:
                         stop=int(round((i+1)*len(trace[1])/chainNum))-1
                    
                    b_val=trace[1][start:stop]
                    bVals.append([b_val])

                    
                for i in range(chainNum):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(bVals[i][0]),np.amax(bVals[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(bVals[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[i],width=2)
                    
                    #Plots the smoothed curve 
                    bPosPlt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.bPosTab=bPosPlt
                        
                self.tabs.addTab(self.bPosTab,"Gaussian Centroid Posterior")
                     
                
                b_traces=pg.PlotWidget()
                b_traces.addLegend()
                b_traces.setMouseEnabled(x=False,y=False)
                
                for i in range(chainNum):
                    x=range(0,len(bVals[0][0]),thin)
                    y=bVals[i][0]
                    y=y[::thin]
    
                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    b_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.bTraceTab=b_traces
                self.tabs.addTab(self.bTraceTab,"Gaussian Centroid Traces")
                
                
                cPosPlt=pg.PlotWidget()
                cVals=[]
                cPosPlt.setMouseEnabled(x=False,y=False)
                
                for i in range(chainNum):
                    start=int(round(i*len(trace[2])/chainNum))
                    stop=int(round((i+1)*len(trace[2])/chainNum))
                    
                    if i==chainNum-1:
                         stop=int(round((i+1)*len(trace[2])/chainNum))-1
                    
                    c_val=trace[2][start:stop]
                    cVals.append([c_val])

                    
                for i in range(chainNum):
                   
                    #Returns the first and last value from the list containing the 
                    #data from each chain
                    chainmin,chainmax=np.amin(cVals[i][0]),np.amax(cVals[i][0])
                    
                    #Creates 200 x values ranging from the first value to the last value
                    x_smooth=np.linspace(chainmin,chainmax,200)
                    
                    #Runs a KDE on the net counts at each x value
                    y_smooth=sp.stats.gaussian_kde(cVals[i])(x_smooth)
                    
                    pen=pg.mkPen(color=colors[i],width=2)
                    
                    #Plots the smoothed curve 
                    cPosPlt.plot(x_smooth,y_smooth,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.cPosTab=cPosPlt
                        
                self.tabs.addTab(self.cPosTab,"Gaussian Sigma Posterior")
                     
                
                c_traces=pg.PlotWidget()
                c_traces.addLegend()
                c_traces.setMouseEnabled(x=False,y=False)
                
                for i in range(chainNum):
                    x=range(0,len(cVals[0][0]),thin)
                    y=cVals[i][0]
                    y=y[::thin]

                    color=pg.intColor(2*i+1, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=150)
                    pen=pg.mkPen(color=color,width=2)
                    c_traces.plot(x,y,pen=pen,antialias=True,name="Chain"+str(i+1))
                
                self.cTraceTab=c_traces
                self.tabs.addTab(self.cTraceTab,"Gaussian Sigma Traces")
                
               
                self.plt.removeItem(self.backReg1)
                self.plt.removeItem(self.backReg2)
                self.plt.removeItem(self.peakReg)
                    
                self.peakSelect.setChecked(False)
                self.backSelec.setChecked(False)
                
                
                
                
                try:
                    minChan=int(self.gaussProb_x1.text())
                    maxChan=int(self.gaussProb_x2.text())
                    
                    Spectrum.Prob(self,[minChan,maxChan],sigCounts,"Gaussian Fit")
                except:
                    if self.gaussProb_x1.text()=="" and self.gaussProb_x2.text()=="":
                        pass
                    else:
                        self.dataWidget.append("Invalid channel region chosen for probability calculation")
                        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
               
           
        if self.gaussFitAction.isChecked()==False:
            
            if self.gaussFitAction.isChecked()==False:
                names=[item.name() for item in self.plt.listDataItems()]
               
                if "gaussFit" in names:
                    
              
        
                    self.mcmcAction.setEnabled(True)
                    self.sumAction.setEnabled(True)
                    
                    
                    pen=pg.mkPen(color="k",width=2)
                    self.plt.clear()
                    self.plot.setData(self.x, self.y,pen=pen,stepMode=True)
                    self.plt.addItem(self.plot)
                    
                    self.peakReg.setRegion((self.xmin,self.xmax))
                    self.plt.addItem(self.peakReg)
            
                
        
   
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                    self.tabs.removeTab(1)
                     
                    self.peakSelect.setChecked(True)
                    
                    self.backReg1.setRegion((self.reg1xmin,self.reg1xmax))
                    self.backReg2.setRegion((self.reg2xmin,self.reg2xmax))
                    self.plt.addItem(self.backReg1)
                    self.plt.addItem(self.backReg2)
                    self.backSelec.setChecked(True)
                
 

                

                

            
            
    def fitRadioButtonClick(self):
        if self.staticSigma.isChecked()==True:
            self.sigmaS=True
            self.sigma.setEnabled(True)
            self.mu.setEnabled(True)
            self.paramSigma.setChecked(False)
        if self.staticSigma.isChecked()==False:
            self.sigmaS=False
            self.sigma.setEnabled(False)
            self.mu.setEnabled(False)

            
        if self.paramSigma.isChecked()==True:
            self.sigmaP=True
            self.staticSigma.setChecked(False)
        if self.paramSigma.isChecked()==False:
            self.sigmaP=False
       
        
    def TestData(self):
        #Creates the window for altering the test data
        testWidget=QDialog()
      
        sample_size = QLineEdit(testWidget)
        peak_location= QLineEdit(testWidget)
        gauss_width=QLineEdit(testWidget)
        bkg_counts=QLineEdit(testWidget)
        min_chan=QLineEdit(testWidget)
        max_chan=QLineEdit(testWidget)
        setSeed=QLineEdit(testWidget)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
        layout = QFormLayout(testWidget)
        layout.addRow("Sample Size: ", sample_size)
        layout.addRow("Location of Peak: ", peak_location)
        layout.addRow("Width of Gaussian: ",gauss_width)
        layout.addRow("Number of Background Counts Per Channel: ",bkg_counts )
        layout.addRow("Minimum Channel: ",min_chan)
        layout.addRow("Maximum Channel: ",max_chan)
        layout.addRow("Set seed: ",setSeed)
        
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(testWidget.accept)
        self.dataWidget.append(
"""
Set parameters for test data. The default paramters used are: """ + 
        """
Sample Size= 1000"""+
        """
Peak Location= Channel 100"""+
        """
Width of Peak= 5"""+
        """
Background Counts Per Channel= 50"""+
       """
Maximum Channel= 200"""+
       """
Minimum Chanel= 0"""+
"""
Seed= 0""")
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
        
        testWidget.exec()
####### Creates a defualt set of paramters to use if the user doesn't choose any
        if sample_size.text()=='':
            sample_size.setText('1000')
            
        if peak_location.text()=='':
            peak_location.setText('100')
            
        if gauss_width.text()=='':
            gauss_width.setText('5')
            
        if bkg_counts.text()=='':
            bkg_counts.setText('50')
            
        if max_chan.text()=='':
            max_chan.setText('200')
            
        if min_chan.text()=='':
            min_chan.setText('0')
            
        if setSeed.text()=='':
            setSeed.setText('0')
        #Converts the user input into the parameters for the test   
        self.sample_size=int(sample_size.text())
        
        self.mean=int(peak_location.text())
        self.width=float(gauss_width.text())

        self.bkg_mean=float(bkg_counts.text())
        self.channel_max=int(max_chan.text())
        self.channel_min=int(min_chan.text())
        
        if self.channel_min>self.channel_max:
            temp=self.channel_min
            self.channel_min=self.channel_max
            self.channel_max=temp
        if self.channel_min==self.channel_max:
            self.channel_max+=10
        
        self.seed=int(setSeed.text())

 
        channel_range=self.channel_max-self.channel_min
        #Sets the number of bins equal to the desired peak width


        np.random.seed(self.seed)
        
        bin_range=list(range(channel_range+1))
        bins=[]
        for i in range(len(bin_range)):
            bin_=int(bin_range[i])+self.channel_min
            bins.append(bin_)
        bins.append(self.channel_max)

        gauss_counts=[]
        for i in range(self.sample_size):
            gauss_count=np.random.normal(self.mean,self.width)
            gauss_counts.append(gauss_count)


        binned_data=[]
        for i in range(len(gauss_counts)):
            count=int(round(gauss_counts[i]))
            binned_data.append(count)


        final_bins=[]


        for i in range(len(bins)):
            bi=binned_data.count(bins[i])
            final_bins.append(bi)
    
        poiss_counts=[]
        for i in range(len(final_bins)):
            p_count=np.random.poisson(final_bins[i])
            poiss_counts.append(p_count)
   
        bkg_counts=[]
        for i in range(len(final_bins)):
            bkg=np.random.poisson(self.bkg_mean)
            bkg_counts.append(bkg)
    
        poiss_counts=np.array(poiss_counts)
        bkg_counts=np.array(bkg_counts)

        total_counts=poiss_counts+bkg_counts


        peak_counts=[]
        peak_bkg=[]
        for i in range(len(final_bins)):
            if poiss_counts[i]>=1:
                peak_counts.append(poiss_counts[i])
                peak_bkg.append(bkg_counts[i])
            
                
       

        #Sums all of the data in the Poisson list, corresponding to the means used
        self.poiss_counts_sum=np.sum(poiss_counts)
        
        counts=np.array(poiss_counts)
        channels=np.array(bins)

        test_mean=np.multiply(counts,channels)
        self.test_centroid=np.sum(test_mean)/(np.sum(counts))
        
            
        self.netSumUnc=(np.sum(peak_counts)+np.sum(peak_bkg))**(1/2)


        x_squared=(channels-self.test_centroid)**2
        xy=np.multiply(x_squared,poiss_counts)
        sum_xy=np.sum(xy)
        N=np.sum(poiss_counts)
        N_1=N-1
        standev=sum_xy/N_1
        standev=(standev)**(1/2)
        self.testStanderr=standev/((N**(1/2)))

        
        
         
        
        #Displays the chosen parameters
        self.dataWidget.append(
"""
PARAMETERS CHOSEN"""+
"""
Sample Size= """+str(self.sample_size)+
"""
Peak Location= Channel= """+str(self.mean)+
        """
Width of Peak= """+str(self.width)+
        """
Background Counts Per Channel= """+str(self.bkg_mean)+
       """
Maximum Channel= """+str(self.channel_max)+
       """
Minimum Channel= """ + str(self.channel_min)+
"""
Seed Used= """+str(self.seed))
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
        
        #Creates a list of the user chosen values and the Poisson sum and centroid
        test_data_values=[self.sample_size,self.mean,self.width,self.bkg_mean,self.channel_max,self.channel_min,self.poiss_counts_sum,self.test_centroid,self.seed]
       
        
        f= open("testing.dat","w+")
        for i in range(len(total_counts)):
            f.write("{0}\t{1}\n".format(channels[i],total_counts[i]))
        parameter_types=["Number of samples","Location of Gaussian","Sigma for Gaussian","Background per channel","End channel","Start channel","Actual signal counts","Actual centroid","Seed used"]
        f.close()
        #Makes a file storing the user selected data
        f=open("test_data_storage.dat","w+")
        for i in range(len(parameter_types)):
            if i==6 or i==7:
                if i==6:
                    f.write((parameter_types[i]+"= %s" % (str(test_data_values[i]))))
                    f.write(" +/- %s\r\n"%(str(self.netSumUnc)))
                if i==7:
                    f.write((parameter_types[i]+"= %s" % (str(test_data_values[i]))))
                    f.write(" +/- %s\r\n"%(str(self.testStanderr)))
            else:
                f.write((parameter_types[i]+"= %s\r\n" % (str(test_data_values[i]))))
        f.close()   
        
    def returnFile(self):
        #Returns the name of the selected file
        clicked_file=self.listWidget.currentItem().text()
        if clicked_file in self.previousfilenames:
            self.previous=True
            #Returns the index of the selected file within the list containing
            #the previous file names
            index=self.previousfilenames.index(clicked_file)
            #Returns the path of the selected file
            self.newfile=self.previousfilepaths[index]
            
            
            self.NewFile()


    def SavePlot(self):

        self.saveWidget=QDialog()
        fileName=QLineEdit(self.saveWidget)
        buttonBox= QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout= QFormLayout(self.saveWidget)
        layout.addRow("Save Plot As: ", fileName)
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.saveWidget.accept)
        buttonBox.rejected.connect(self.saveWidget.reject)
        
        self.saveWidget.exec()

        if fileName.text()!="":

            file_name=str(fileName.text())
        
            exporter = pg.exporters.ImageExporter(self.plt.plotItem)
            exporter.params.param('width').setValue(1920, blockSignal=exporter.widthChanged)
            exporter.params.param('height').setValue(1080, blockSignal=exporter.heightChanged)
            exporter.export(file_name+".png")
            
            self.dataWidget.append(
""" 
"""+
str(file_name)+".png saved")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
            
            
            
    def RefreshSideBar(self):
        f=open("used_file_storage.txt","w")
        f.close()
        
        self.previousfilepaths.clear()
        self.previousfilenames.clear()
                    
        self.listWidget.clear()
        
        self.dataWidget.append(
""" 
"""+
"Files cleared from sidebar")
        self.dataWidget.moveCursor(QtGui.QTextCursor.End)
        
        
        
    def CalibrateEnergy(self):
        try:
            CallibrationSlope=float(self.energyCallibrationSlope.text())
            CallibrationIntercept=float(self.energyCallibrationIntercept.text())
            self.energyCallibrationParamters.clear()
            self.energyCallibrationParamters.append([CallibrationSlope,CallibrationIntercept])
        
            self.dataWidget.append(
"""
Energy calibrated""")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
            
        except:
            self.energyCallibrationParamters.clear()
            self.energy_label.setText("Energy=NA")
            self.dataWidget.append(
"""
Error occured while calibrating energy""")
            self.dataWidget.moveCursor(QtGui.QTextCursor.End)
            
            
        
        
        
    
            
            
            
