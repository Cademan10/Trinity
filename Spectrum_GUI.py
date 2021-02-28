from Data_Handler import *
    
class MainWindow(Spectrum):
    def __init__(self):
         pg.setConfigOption("background", "w")
         pg.setConfigOption("foreground", "k")
         Spectrum.__init__(self)

#Creates GUI Application
if __name__ == '__main__':
    app = QApplication.instance()
    if app==None:
        app=QApplication([])
    
    
    
    main = MainWindow()
    main.setGeometry(100,100,1300,800)
    main.setWindowTitle("Trinity")
    
    
    main.setWindowIcon(QtGui.QIcon(icondir+'TrinityLogo.png')) 

    
    
    main.show()  
    
    

    sys.exit(app.exec_())
    
