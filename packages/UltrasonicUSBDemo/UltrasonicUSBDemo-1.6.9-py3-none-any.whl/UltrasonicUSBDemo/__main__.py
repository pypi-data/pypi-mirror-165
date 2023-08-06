import sys
import os.path
import pkg_resources
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
#from . import Ui_UltrasonicUSBDemoUI
#from Ui_UltrasonicUSBDemoUI import Ui_MainWindow
import serial
import glob
import os
import socket
from xml.etree import ElementTree
#from ValueDialog import Ui_Dialog
from datetime import datetime


UM0034 = 0
UM0017 = 1
UM0090 = 2
FS000x = 3
FS0002 = 4


#from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 673)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.demoTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.demoTypeComboBox.setObjectName("demoTypeComboBox")
        self.demoTypeComboBox.addItem("")
        self.demoTypeComboBox.addItem("")
        self.demoTypeComboBox.addItem("")
        self.demoTypeComboBox.addItem("")
        self.demoTypeComboBox.addItem("")
        self.horizontalLayout.addWidget(self.demoTypeComboBox)
        self.ComPortComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.ComPortComboBox.setObjectName("ComPortComboBox")
        self.horizontalLayout.addWidget(self.ComPortComboBox)
        self.ComOpen = QtWidgets.QPushButton(self.centralwidget)
        self.ComOpen.setObjectName("ComOpen")
        self.horizontalLayout.addWidget(self.ComOpen)
        self.rescanButton = QtWidgets.QPushButton(self.centralwidget)
        self.rescanButton.setObjectName("rescanButton")
        self.horizontalLayout.addWidget(self.rescanButton)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelImage = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImage.sizePolicy().hasHeightForWidth())
        self.labelImage.setSizePolicy(sizePolicy)
        self.labelImage.setMaximumSize(QtCore.QSize(16777213, 16777215))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.horizontalLayout_3.addWidget(self.labelImage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ReceiveMemo = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ReceiveMemo.setReadOnly(True)
        self.ReceiveMemo.setMaximumBlockCount(1000)
        self.ReceiveMemo.setCenterOnScroll(True)
        self.ReceiveMemo.setObjectName("ReceiveMemo")
        self.horizontalLayout_2.addWidget(self.ReceiveMemo)
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.horizontalLayout_2.addLayout(self.buttonLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ultrasonic USB Demo           Version 1.6.9"))
        self.demoTypeComboBox.setItemText(0, _translate("MainWindow", "UM0034-002 Proximity"))
        self.demoTypeComboBox.setItemText(1, _translate("MainWindow", "UM0017 Water Level"))
        self.demoTypeComboBox.setItemText(2, _translate("MainWindow", "UM0090 Proximity"))
        self.demoTypeComboBox.setItemText(3, _translate("MainWindow", "FS000x Smart Flow Meter"))
        self.demoTypeComboBox.setItemText(4, _translate("MainWindow", "FS0002 Smart Flow Meter"))
        self.ComOpen.setText(_translate("MainWindow", "Open"))
        self.rescanButton.setText(_translate("MainWindow", "ReScan"))

 



def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class commVariables(object):
    def __init__(self):
        self.demoType = 0
        self.accessnumber = 0
        self.UltrasonicParmList = []
        self.receive_index = 0
        self.receive_buffer = [0] * 256
        self.read_index = 0
        self.Received_ok = False
        self.Received_badcmd = False
        self.ser = serial.Serial()
        self.elapsed_time = ""
        self.wait_reply_timer = 10
        self.update_index = 0
        self.tickcount = 20
        self.logtickcount = 5
        self.runsecs = 0
        self.runmins = 0
        self.runhrs = 0
#        self.logfilename = ""
        self.togglemode = 0


def isportopen():
    global gcvars
    if(serial.VERSION == '2.7'):
        return(gcvars.ser.isOpen())
    else:
        return(gcvars.ser.is_open)

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

class UltrasonicParameter(object):
    def __init__(self):
        self.index = 0
        self.readonly = 0
        self.showhex = 0
        self.value = 0
        self.mask = 0
        self.name = ""
        self.skipnext = False
        self.needsUpdate = False


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        global gcvars
        gcvars = commVariables()

        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.ComOpen.pressed.connect(lambda n="call": self.ComOpenClick(n))
        self.ui.rescanButton.pressed.connect(lambda n="call": self.ButtonRescan_Click(n))
#        self.ui.addButton = QtWidgets.QPushButton('mybutton')
        self.ui.demoTypeComboBox.currentIndexChanged.connect(self.demoChanged)
        self.ui.ComPortComboBox.clear()

        list_ports = serial_ports()
        for x in list_ports:
            self.ui.ComPortComboBox.addItem(x)
        self.ui.ComPortComboBox.setCurrentIndex(0)


        self.ui.parmlabel = {}
        self.ui.parmbutton = {}


        self.demoChanged()

        # target_index = 0
        # file_available = False
        # while((file_available==False)and(target_index < 10000)):

        #     trycsvname = "logs/fs000x."+str(target_index)+".csv"
        #     if(os.path.isfile(trycsvname)==False):
        #         gcvars.logfilename = trycsvname
        #         file_available = True
        #     else:
        #         target_index = target_index + 1
        # if(not file_available):
        #     gcvars.logfilename = "logs/fs000x.xxxx.csv"
        # with open(gcvars.logfilename, 'w') as out:
        #     index = 0
        #     out.write('Local Time,')
        #     for x in gcvars.UltrasonicParmList :
        #         out.write(str(x.name)+',')
        #     out.write('\r');


    def demoChanged(self):
        # close the port if it is open
        gcvars.receive_index = 0;
        gcvars.receive_buffer = [0] * 256
        if(isportopen()):
            gcvars.ser.flushOutput()
            gcvars.ser.flushInput()
            self.ui.ReceiveMemo.appendPlainText("Closing Port")
            gcvars.ser.close()
            self.ui.ComOpen.setText("Open")
        print("Demo Changed to "+self.ui.demoTypeComboBox.currentText())
        demo_index = self.ui.demoTypeComboBox.currentIndex()        
        print("Demo index is now "+str(demo_index))
        gcvars.demoType = demo_index

        clearLayout(self.ui.buttonLayout)
        self.ui.buttonFrame = QtWidgets.QFrame()
        self.ui.buttonLayout.addWidget(self.ui.buttonFrame)

        self.ui.parmlabel.clear()
        self.ui.parmbutton.clear()
        gcvars.UltrasonicParmList.clear()

        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the pyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
            print('not frozen : '+application_path)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            print('frozen : '+application_path)


        print(os.path.dirname(__file__))

        if(gcvars.demoType == UM0034):
#            fn = os.path.join(application_path, 'image/um0034_banner.png')
            fn = os.path.join(application_path, pkg_resources.resource_filename(__name__, 'image/um0034_banner.png'))
            self.ui.labelImage.setPixmap(QPixmap(fn))
            newparm = UltrasonicParameter()
            newparm.index = 0
            newparm.readonly = 1
            newparm.showhex = 0
            newparm.value = 0
            newparm.name = "Distance (mm)"
            gcvars.UltrasonicParmList.append(newparm)
            xloc = 10
            yloc = 5
            self.ui.parmlabel[0] = QtWidgets.QLabel(self.ui.buttonFrame)
            self.ui.parmlabel[0].setGeometry(QtCore.QRect(xloc, yloc, 120, 25))
            self.ui.parmlabel[0].setObjectName("labelp")
            self.ui.parmlabel[0].setText(newparm.name)
            self.ui.parmlabel[0].show()
            self.ui.parmbutton[0] = QtWidgets.QPushButton(self.ui.buttonFrame)
            self.ui.parmbutton[0].setGeometry(QtCore.QRect(xloc+130, yloc, 120, 25))
            self.ui.parmbutton[0].setText('{0:d}'.format(newparm.value))
            self.ui.parmbutton[0].show()

        elif(gcvars.demoType == UM0017):
#            fn = os.path.join(application_path, 'image/um0017_banner.png')
            fn = os.path.join(application_path, pkg_resources.resource_filename(__name__, 'image/um0017_banner.png'))
            self.ui.labelImage.setPixmap(QPixmap(fn))
            newparm = UltrasonicParameter()
            newparm.index = 0
            newparm.readonly = 1
            newparm.showhex = 0
            newparm.value = 0
            newparm.name = "Level (mm)"
            gcvars.UltrasonicParmList.append(newparm)
            xloc = 10
            yloc = 5
            self.ui.parmlabel[0] = QtWidgets.QLabel(self.ui.buttonFrame)
            self.ui.parmlabel[0].setGeometry(QtCore.QRect(xloc, yloc, 120, 25))
            self.ui.parmlabel[0].setObjectName("labelp")
            self.ui.parmlabel[0].setText(newparm.name)
            self.ui.parmlabel[0].show()
            self.ui.parmbutton[0] = QtWidgets.QPushButton(self.ui.buttonFrame)
            self.ui.parmbutton[0].setGeometry(QtCore.QRect(xloc+130, yloc, 120, 25))
            self.ui.parmbutton[0].setText('{0:d}'.format(newparm.value))
            self.ui.parmbutton[0].show()

        elif(gcvars.demoType == UM0090):
#            fn = os.path.join(application_path, 'image/um0090_banner.png')
            fn = os.path.join(application_path, pkg_resources.resource_filename(__name__, 'image/um0090_banner.png'))
            self.ui.labelImage.setPixmap(QPixmap(fn))
            newparm = UltrasonicParameter()
            newparm.index = 0
            newparm.readonly = 1
            newparm.showhex = 0
            newparm.value = 0
            newparm.name = "Distance (cm)"
            gcvars.UltrasonicParmList.append(newparm)
            xloc = 10
            yloc = 5
            self.ui.parmlabel[0] = QtWidgets.QLabel(self.ui.buttonFrame)
            self.ui.parmlabel[0].setGeometry(QtCore.QRect(xloc, yloc, 120, 25))
            self.ui.parmlabel[0].setObjectName("labelp")
            self.ui.parmlabel[0].setText(newparm.name)
            self.ui.parmlabel[0].show()
            self.ui.parmbutton[0] = QtWidgets.QPushButton(self.ui.buttonFrame)
            self.ui.parmbutton[0].setGeometry(QtCore.QRect(xloc+130, yloc, 120, 25))
            self.ui.parmbutton[0].setText('{0:d}'.format(newparm.value))
            self.ui.parmbutton[0].show()

        elif(gcvars.demoType == FS000x):
#            fn = os.path.join(application_path, 'image/fs000x_banner.png')
            fn = os.path.join(application_path, pkg_resources.resource_filename(__name__, 'image/fs000x_banner.png'))
            self.ui.labelImage.setPixmap(QPixmap(fn))
            fn = os.path.join(application_path, 'fs000x.xml')

            with open(fn, 'rt') as f:
                tree = ElementTree.parse(f)
                root = tree.getroot()
                for child in root.iter('parameter'):
                    newparm = UltrasonicParameter()
                    newparm.index = int(child.attrib['index'])
                    newparm.readonly = int(child.attrib['readonly'])
                    newparm.showhex = int(child.attrib['showhex'])
                    newparm.value = int(child.attrib['initval'])
                    newparm.name = child.text
                    gcvars.UltrasonicParmList.append(newparm)
                    print(newparm.index, child.text)

            for item in gcvars.UltrasonicParmList:
                print(item.index, item.readonly, item.showhex, item.value)


            for node in gcvars.UltrasonicParmList:
                xloc = 10 + (node.index // 20)*240
                yloc = 5 + (node.index % 25)*30
                self.ui.parmlabel[node.index] = QtWidgets.QLabel(self.ui.buttonFrame)
                self.ui.parmlabel[node.index].setGeometry(QtCore.QRect(xloc, yloc, 120, 25))
                self.ui.parmlabel[node.index].setObjectName("labelp")
                self.ui.parmlabel[node.index].setText(node.name)
                self.ui.parmlabel[node.index].show()
                self.ui.parmbutton[node.index] = QtWidgets.QPushButton(self.ui.buttonFrame)
                self.ui.parmbutton[node.index].setGeometry(QtCore.QRect(xloc+130, yloc, 120, 25))
                self.ui.parmbutton[node.index].setText('{0:d}'.format(node.value))
                self.ui.parmbutton[node.index].show()

#            self.ui.togglemodebutton = QtWidgets.QPushButton(self.ui.buttonFrame)
#            self.ui.togglemodebutton.setGeometry(QtCore.QRect(260, 5, 100, 25))
#            self.ui.togglemodebutton.setText('MToggle')
#            self.ui.togglemodebutton.show()
#            self.ui.togglemodebutton.pressed.connect(lambda n="call": self.ToggleModeButton(n))

#            self.ui.resetaccbutton = QtWidgets.QPushButton(self.ui.buttonFrame)
#            self.ui.resetaccbutton.setGeometry(QtCore.QRect(260, 35, 100, 25))
#            self.ui.resetaccbutton.setText('ResetAcc')
#            self.ui.resetaccbutton.show()
#            self.ui.resetaccbutton.pressed.connect(lambda n="call": self.ResetAccButton(n))


        elif(gcvars.demoType == FS0002):
            fn = os.path.join(application_path, 'image/fs000x_banner.png')
            self.ui.labelImage.setPixmap(QPixmap(fn))
            fn = os.path.join(application_path, 'fs0002.xml')

            with open(fn, 'rt') as f:
                tree = ElementTree.parse(f)
                root = tree.getroot()
                for child in root.iter('parameter'):
                    newparm = UltrasonicParameter()
                    newparm.index = int(child.attrib['index'])
                    newparm.readonly = int(child.attrib['readonly'])
                    newparm.showhex = int(child.attrib['showhex'])
                    newparm.value = int(child.attrib['initval'])
                    newparm.name = child.text
                    gcvars.UltrasonicParmList.append(newparm)
                    print(newparm.index, child.text)

            for item in gcvars.UltrasonicParmList:
                print(item.index, item.readonly, item.showhex, item.value)


            for node in gcvars.UltrasonicParmList:
                xloc = 10 + (node.index // 20)*240
                yloc = 5 + (node.index % 25)*30
                self.ui.parmlabel[node.index] = QtWidgets.QLabel(self.ui.buttonFrame)
                self.ui.parmlabel[node.index].setGeometry(QtCore.QRect(xloc, yloc, 120, 25))
                self.ui.parmlabel[node.index].setObjectName("labelp")
                self.ui.parmlabel[node.index].setText(node.name)
                self.ui.parmlabel[node.index].show()
                self.ui.parmbutton[node.index] = QtWidgets.QPushButton(self.ui.buttonFrame)
                self.ui.parmbutton[node.index].setGeometry(QtCore.QRect(xloc+130, yloc, 100, 25))
                self.ui.parmbutton[node.index].setText('{0:d}'.format(node.value))
                self.ui.parmbutton[node.index].show()

            self.ui.togglemodebutton = QtWidgets.QPushButton(self.ui.buttonFrame)
            self.ui.togglemodebutton.setGeometry(QtCore.QRect(250, 5, 100, 25))
            self.ui.togglemodebutton.setText('MToggle')
            self.ui.togglemodebutton.show()
            self.ui.togglemodebutton.pressed.connect(lambda n="call": self.ToggleModeButton(n))



    def ToggleModeButton(self, s):
        global gcvars
        if(isportopen()):

            print("Transmitting Toggle : "+format(gcvars.togglemode))
            out_buffer = ""
            if(gcvars.togglemode == 0):
               temp_buffer = chr(0x10) + chr(0x5C) + chr(0x00) + chr(0x5C) +chr(0x16)
               gcvars.togglemode = 1
            else:
               temp_buffer = chr(0x10) + chr(0x5C) + chr(0x01) + chr(0x5D) +chr(0x16)
               gcvars.togglemode = 0

            for i in range(0,96):
                temp_buffer = chr(0xFE) + temp_buffer
            self.ui.ReceiveMemo.appendPlainText('Sending : '+"".join(format(ord(x),'02x') for x in temp_buffer[96:]))
            packet = bytearray()
            for x in temp_buffer :
                packet.append(ord(x))
            gcvars.ser.write(packet)
           
            gcvars.ser.flushOutput()


    def ComOpenClick(self, s):
        global gcvars
        if(isportopen()):
            #        if(gcvars.ser.isOpen()):
            self.ui.ReceiveMemo.appendPlainText("Closing Port")
            gcvars.ser.close()
            self.ui.ComOpen.setText("Open")
        else:
            self.ui.ReceiveMemo.appendPlainText("Opening Port")
            self.ui.ComOpen.setText("Close")
            comportname = self.ui.ComPortComboBox.currentText()
            self.ui.ReceiveMemo.appendPlainText(comportname)
            gcvars.ser.port = comportname
            if(gcvars.demoType == UM0034):
                gcvars.ser.baudrate = 9600
                gcvars.ser.parity = 'N'
            if(gcvars.demoType == UM0017):
                gcvars.ser.baudrate = 9600
                gcvars.ser.parity = 'N'
            if(gcvars.demoType == UM0090):
                gcvars.ser.baudrate = 9600
                gcvars.ser.parity = 'N'
            if(gcvars.demoType == FS000x):
                gcvars.ser.baudrate = 115200
                gcvars.ser.parity = 'E'
            if(gcvars.demoType == FS0002):
                gcvars.ser.baudrate = 9600
                gcvars.ser.parity = 'E'
            
            gcvars.ser.open()

    def ButtonRescan_Click(self, s):
        global gcvars
        if(isportopen()):
            self.ui.ReceiveMemo.appendPlainText("Closing Port")
            gcvars.ser.close()
        self.ui.ComPortComboBox.clear()
        list_ports = serial_ports()
        for x in list_ports:
            self.ui.ComPortComboBox.addItem(x)
        self.ui.ComPortComboBox.setCurrentIndex(0)

    def format_outmessage(self, instr, strlen):
        if isportopen() :
#        if(gcvars.ser.is_open):
            #        if(gcvars.ser.isOpen()):
            print("Transmitting : ",instr)
            out_csum = 0
            out_buffer = ""
            for from_index in range(0, strlen):
                out_buffer = out_buffer + instr[from_index]
                out_csum = out_csum + ord(instr[from_index])
            if strlen == 1 : 
                out_buffer = out_buffer + chr(0xFD)
                out_csum = out_csum + 0xFD
            temp_buffer = chr(0x10) + out_buffer + chr(out_csum & 0xFF) + chr(0x16)

            for i in range(0,96):
                temp_buffer = chr(0xFE) + temp_buffer
            self.ui.ReceiveMemo.appendPlainText('Sending : '+"".join(format(ord(x),'02x') for x in temp_buffer[96:]))
            packet = bytearray()
            for x in temp_buffer :
#                print(ord(x))
                packet.append(ord(x))
#            for x in temp_buffer :
            gcvars.ser.write(packet)
#            self.ui.ReceiveMemo.appendPlainText(''.join(format(x, '02x') for x in temp_buffer.encode('utf-8')))
#            for i in range(0,40) :
#                gcvars.ser.write(0xFE)
#            gcvars.ser.write(temp_buffer.encode('utf-8'))
            
            gcvars.ser.flushOutput()


    def format_fs000x_outmessage(self, instr, strlen):
        if isportopen() :
#        if(gcvars.ser.is_open):
            #        if(gcvars.ser.isOpen()):
            print("Transmitting : ",instr)
            out_csum = 0
            out_buffer = ""
            for from_index in range(0, strlen):
                out_buffer = out_buffer + instr[from_index]
                out_csum = out_csum + ord(instr[from_index])
            if strlen == 1 : 
                out_buffer = out_buffer + chr(0xFD)
                out_csum = out_csum + 0xFD
            temp_buffer = chr(0x10) + out_buffer + chr(out_csum & 0xFF) + chr(0x16)

            for i in range(0,96):
                temp_buffer = chr(0xFE) + temp_buffer
            self.ui.ReceiveMemo.appendPlainText('Sending : '+"".join(format(ord(x),'02x') for x in temp_buffer[96:]))
            packet = bytearray()
            for x in temp_buffer :
                packet.append(ord(x))
            gcvars.ser.write(packet)
           
            gcvars.ser.flushOutput()

    def format_fs0002_outmessage(self, instr, strlen):
        if isportopen() :
#        if(gcvars.ser.is_open):
            #        if(gcvars.ser.isOpen()):
            print("Transmitting : ",instr)
            out_csum = 0
            out_buffer = ""
            for from_index in range(0, strlen):
                out_buffer = out_buffer + instr[from_index]
                out_csum = out_csum + ord(instr[from_index])
            if strlen == 1 : 
                out_buffer = out_buffer + chr(0xFD)
                out_csum = out_csum + 0xFD
            temp_buffer = chr(0x10) + out_buffer + chr(out_csum & 0xFF) + chr(0x16)

#            for i in range(0,96):
#                temp_buffer = chr(0xFE) + temp_buffer
            self.ui.ReceiveMemo.appendPlainText('Sending : '+"".join(format(ord(x),'02x') for x in temp_buffer))
            packet = bytearray()
            for x in temp_buffer :
                packet.append(ord(x))
            gcvars.ser.write(packet)
           
            gcvars.ser.flushOutput()


    def tick(self):
        global gcvars
        if(gcvars.tickcount > 0):
            gcvars.tickcount -= 1
        else:
            gcvars.tickcount = 20

            # if(gcvars.logtickcount > 0):
            #     gcvars.logtickcount -= 1
            # else:
            #     gcvars.logtickcount = 10

                # # log at 10 second intervals
                # if isportopen():
                #     with open(gcvars.logfilename, 'a') as out:
                #         out.write(str(datetime.now())+",")
                #         for x in gcvars.UltrasonicParmList :
                #             out.write(str(x.value)+',')
                #         out.write('\r');

        if(gcvars.wait_reply_timer > 0):
            gcvars.wait_reply_timer -= 1

        if isportopen():
            while(gcvars.ser.inWaiting() > 0):
                char = gcvars.ser.read(1)
                gcvars.receive_buffer[gcvars.receive_index] = ord(char)
                print(hex(ord(char))+" "+str(ord(char)))
#                print(ord(char))
#                print(char)
                gcvars.receive_index += 1
                gcvars.receive_index &= 0xFF
            # end while serial char to read


            # do we need to kick off a transmission to the device?
            if(gcvars.wait_reply_timer == 0):
                gcvars.wait_reply_timer = 40 # two seconds
                # will eventually need to send commands other than an update request, but for now, that's all we have
                if(gcvars.demoType == FS000x):
                    self.format_fs000x_outmessage('[',1)
                elif(gcvars.demoType == FS0002):
                    if(gcvars.togglemode == 0):                    
                        self.format_fs0002_outmessage('[',1)
                else:
                    print("Transmitting : T")
                    gcvars.ser.write(ord('T'))
                    gcvars.ser.flushOutput()

            if(gcvars.demoType == FS0002):
                self.parseReceive_fs0002()
            if(gcvars.demoType == FS000x):
                self.parseReceive_fs000x()
            if(gcvars.demoType == UM0090):
                self.parseReceive_um0090()
            if(gcvars.demoType == UM0017):
                self.parseReceive_um0017()
            if(gcvars.demoType == UM0034):
                self.parseReceive_um0034()
        
    def parseReceive_um0034(self):
        starttokenfound = False
        endtokenfound = False
        check_index = 0
        check_end_index = 0
        look_buffer = [0] * 256
        look_buffer_index = 0
        input_checksum = 0
        temp_substring = ""
        getindex = 0
        index = 0
        if(gcvars.read_index != gcvars.receive_index):
#                print('Read Index = {0}, Receive Index = {1}'.format(gcvars.read_index,gcvars.receive_index))
            check_index = gcvars.read_index
            starttokenfound = False
            while check_index != gcvars.receive_index and not starttokenfound:
                if gcvars.receive_buffer[check_index] != ord('='):
#                if ord(gcvars.receive_buffer[check_index]) != ord('n') :
                    # discard characters that aren't start of message
                    check_index += 1
                    check_index &= 0xFF
                    gcvars.read_index += 1
                    gcvars.read_index &= 0xFF
                else:
                    # Got a potential message to parse
                    print('Got Start of Message')
                    starttokenfound = True
                    check_end_index = check_index
                    endtokenfound = False
                    while (check_end_index != gcvars.receive_index) and (not endtokenfound):
                        look_buffer[look_buffer_index] = gcvars.receive_buffer[check_end_index]
                        look_buffer_index += 1
                        if gcvars.receive_buffer[check_end_index] != 0xFF :
                            check_end_index += 1
                            check_end_index &= 0xFF
                        else:
                            self.ui.ReceiveMemo.appendPlainText('Received : '+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                            print('Got end of message')
                            gcvars.read_index = check_end_index + 1
                            gcvars.read_index &= 0xFF
                            endtokenfound = True
                            if look_buffer_index > 3:

                                gcvars.UltrasonicParmList[0].value = 0
                                for x in range(1,look_buffer_index-1):
                                    gcvars.UltrasonicParmList[0].value *= 10
                                    gcvars.UltrasonicParmList[0].value += look_buffer[x]-ord('0')
                                    print(gcvars.UltrasonicParmList[0].value)

                                self.ui.parmbutton[0].setText(str(gcvars.UltrasonicParmList[0].value))
                                gcvars.wait_reply_timer = 10         
 

    def parseReceive_um0017(self):
        starttokenfound = False
        endtokenfound = False
        check_index = 0
        check_end_index = 0
        look_buffer = [0] * 256
        look_buffer_index = 0
        input_checksum = 0
        temp_substring = ""
        getindex = 0
        index = 0

        if(gcvars.read_index != gcvars.receive_index):
#                print('Read Index = {0}, Receive Index = {1}'.format(gcvars.read_index,gcvars.receive_index))
            check_index = gcvars.read_index
            starttokenfound = False
            while check_index != gcvars.receive_index and not starttokenfound:
                if gcvars.receive_buffer[check_index] == 0xFF:
                    # discard characters that aren't start of message
                    check_index += 1
                    check_index &= 0xFF
                    gcvars.read_index += 1
                    gcvars.read_index &= 0xFF
                else:
                    # Got a potential message to parse
#                        print('Got Start of Message')
                    starttokenfound = True
                    check_end_index = check_index
                    endtokenfound = False
                    while (check_end_index != gcvars.receive_index) and (not endtokenfound):
                        look_buffer[look_buffer_index] = gcvars.receive_buffer[check_end_index]
                        look_buffer_index += 1
                        if look_buffer_index > 20:
                            # overflow exit
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                            print('Overflow, length is ',look_buffer_index)
                        elif gcvars.receive_buffer[check_end_index] != 0xFF and look_buffer_index > 3:
                            print('Bad End Char ',gcvars.receive_buffer[check_end_index],' length is ',look_buffer_index)
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                        elif look_buffer_index < 3:
#                                print('Adding Char ',ord(gcvars.receive_buffer[check_end_index]),' length is ',len(look_buffer))
                            check_end_index += 1
                            check_end_index &= 0xFF
                        else:
                            print('Got end of message')
                            
                            gcvars.read_index = check_end_index + 1
                            gcvars.read_index &= 0xFF
                            endtokenfound = True
                            if look_buffer_index > 2:
                                print("".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                                if(gcvars.UltrasonicParmList[0].skipnext):
                                    gcvars.UltrasonicParmList[0].skipnext = False
                                    self.ui.ReceiveMemo.appendPlainText('Received : '+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))

                                    gcvars.UltrasonicParmList[0].value = 0
                                    for x in range(2,-1,-1):
                                        print(look_buffer[x])
                                        gcvars.UltrasonicParmList[0].value *= 256
                                        gcvars.UltrasonicParmList[0].value += look_buffer[x]
                                        print(gcvars.UltrasonicParmList[0].value)

                                    self.ui.parmbutton[0].setText(str(gcvars.UltrasonicParmList[0].value))


                                    gcvars.wait_reply_timer = 10         
                                else:                                   
                                    gcvars.UltrasonicParmList[0].skipnext = True




    def parseReceive_um0090(self):
        starttokenfound = False
        endtokenfound = False
        check_index = 0
        check_end_index = 0
        look_buffer = [0] * 256
        look_buffer_index = 0
        input_checksum = 0
        temp_substring = ""
        getindex = 0
        index = 0

        if(gcvars.read_index != gcvars.receive_index):
#                print('Read Index = {0}, Receive Index = {1}'.format(gcvars.read_index,gcvars.receive_index))
            check_index = gcvars.read_index
            starttokenfound = False
            while check_index != gcvars.receive_index and not starttokenfound:
                if gcvars.receive_buffer[check_index] != ord('='):
                    # discard characters that aren't start of message
                    check_index += 1
                    check_index &= 0xFF
                    gcvars.read_index += 1
                    gcvars.read_index &= 0xFF
                else:
                    # Got a potential message to parse
#                        print('Got Start of Message')

                    starttokenfound = True
                    check_end_index = check_index
                    endtokenfound = False
                    while (check_end_index != gcvars.receive_index) and (not endtokenfound):
                        look_buffer[look_buffer_index] = gcvars.receive_buffer[check_end_index]
                        look_buffer_index += 1
                        if look_buffer_index > 20:
                            # overflow exit
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                            print('Overflow, length is ',look_buffer_index)
                        elif gcvars.receive_buffer[check_end_index] != 0xFF and look_buffer_index > 4:
                            print('Bad End Char ',gcvars.receive_buffer[check_end_index],' length is ',look_buffer_index)
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                        elif look_buffer_index < 4:
#                                print('Adding Char ',ord(gcvars.receive_buffer[check_end_index]),' length is ',len(look_buffer))
                            check_end_index += 1
                            check_end_index &= 0xFF
                        else:
                            print('Got end of message')
                            
                            gcvars.read_index = check_end_index + 1
                            gcvars.read_index &= 0xFF
                            endtokenfound = True
                            if look_buffer_index > 3:
                                print("".join(format(x,'02x') for x in look_buffer))
                                if(gcvars.UltrasonicParmList[0].skipnext):
                                    gcvars.UltrasonicParmList[0].skipnext = False
                                    self.ui.ReceiveMemo.appendPlainText('Received : '+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))

                                    gcvars.UltrasonicParmList[0].value = 0
                                    for x in range(1,4):
                                         gcvars.UltrasonicParmList[0].value *= 10
                                         gcvars.UltrasonicParmList[0].value += look_buffer[x]-ord('0')

                                    self.ui.parmbutton[0].setText(str(gcvars.UltrasonicParmList[0].value))


                                    gcvars.wait_reply_timer = 10         
                                else:                                   
                                    gcvars.UltrasonicParmList[0].skipnext = True
                                        

    def parseReceive_fs0002(self):
        starttokenfound = False
        endtokenfound = False
        check_index = 0
        check_end_index = 0
        look_buffer = [0] * 256
        look_buffer_index = 0
        input_checksum = 0
        temp_substring = ""
        getindex = 0
        index = 0

        if(gcvars.read_index != gcvars.receive_index):
#                print('Read Index = {0}, Receive Index = {1}'.format(gcvars.read_index,gcvars.receive_index))
            check_index = gcvars.read_index
            starttokenfound = False



            while check_index != gcvars.receive_index and not starttokenfound:
                if gcvars.receive_buffer[check_index] != 0x42:
                    # discard characters that aren't start of message
                    check_index += 1
                    check_index &= 0xFF
                    gcvars.read_index += 1
                    gcvars.read_index &= 0xFF
                else:
                    # Got a potential message to parse
                    print('Got Start of Message')
                    starttokenfound = True
                    check_end_index = check_index
                    endtokenfound = False
                    while (check_end_index != gcvars.receive_index) and (not endtokenfound):
                        look_buffer[look_buffer_index] = gcvars.receive_buffer[check_end_index]
                        look_buffer_index += 1
                        if look_buffer_index > 32:
                            # overflow exit
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                            print('Overflow, length is ',look_buffer_index)
                        elif gcvars.receive_buffer[check_end_index] != 0x16 and look_buffer_index == 32:
                            print('Bad End Char ',gcvars.receive_buffer[check_end_index],' length is ',look_buffer_index)
                            print("".join(format(x,'02x') for x in look_buffer[0:look_buffer_index-1]))
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                        elif look_buffer_index < 32:
#                                print('Adding Char ',ord(gcvars.receive_buffer[check_end_index]),' length is ',len(look_buffer))
                            check_end_index += 1
                            check_end_index &= 0xFF
                        else:
                            print('Got end of message')
                            
                            gcvars.read_index = check_end_index + 1
                            gcvars.read_index &= 0xFF
                            endtokenfound = True
                            if look_buffer_index > 4:
                                print("".join(format(x,'02x') for x in look_buffer[:32]))
                                checksum_valid = True
                                try:
                                    input_checksum = look_buffer[30]
                                    print('Input Checksum is ',input_checksum,' length is ',look_buffer_index)
                                except:
                                    self.ui.ReceiveMemo.appendPlainText('ERROR - input checksum invalid format '+look_buffer)
                                    checksum_valid = False
                                print(input_checksum)
                                read_checksum = 0
                                for index in range(2, look_buffer_index-3):
                                    read_checksum += look_buffer[index]
                                read_checksum &= 0xFF
                                print("readcsum1",read_checksum)

                                read_checksum2 = 0
                                for index in range(0, look_buffer_index-2):
                                    read_checksum2 += look_buffer[index]
                                read_checksum2 &= 0xFF
                                print("readcsum2",read_checksum2)
                                if(input_checksum == read_checksum):
                                    print("csumorg")
                                elif(input_checksum == read_checksum2):
                                    print("csumnew")
                                if(input_checksum == read_checksum)or(input_checksum==read_checksum2):
                                    print("".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                                    self.ui.ReceiveMemo.appendPlainText('Received : '+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                                    gcvars.UltrasonicParmList[0].value = look_buffer[5]
                                    self.ui.parmbutton[0].setText(str(look_buffer[5]))

                                    # Device ID
                                    gcvars.UltrasonicParmList[0].value = 0
                                    for x in range(2,7):
                                        gcvars.UltrasonicParmList[0].value *= 256
                                        gcvars.UltrasonicParmList[0].value += look_buffer[x]
                                    self.ui.parmbutton[0].setText(str(format(gcvars.UltrasonicParmList[0].value,"08x")))

                                    # Version
                                    gcvars.UltrasonicParmList[1].value = look_buffer[7]
                                    self.ui.parmbutton[1].setText(str(look_buffer[7]))

                                    # Status Byte
                                    gcvars.UltrasonicParmList[2].value = look_buffer[29]
                                    self.ui.parmbutton[2].setText(str(format(gcvars.UltrasonicParmList[2].value,"02x")))


                                    # Acc. Flow
                                    gcvars.UltrasonicParmList[3].value = 0
                                    multiplier = 1
                                    for x in range(9,15):
                                        tempval = look_buffer[x]
#                                        print('A'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[3].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[3].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[3].setText(str(gcvars.UltrasonicParmList[3].value/1000.0))

                                    # Ins. Flow
                                    gcvars.UltrasonicParmList[4].value = 0
                                    multiplier = 1
                                    for x in range(16,20):
                                        tempval = look_buffer[x]
#                                        print('I'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[4].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[4].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[4].setText(str(gcvars.UltrasonicParmList[4].value/100.0))
#                                    with open(gcvars.logfilename, 'a') as out:
#                                        out.write(str(datetime.now())+",")
#                                        out.write(str(gcvars.UltrasonicParmList[4].value/100.0))
#                                        out.write('\r');

                                    # Acc. Time
                                    gcvars.UltrasonicParmList[5].value = 0
                                    multiplier = 1
                                    for x in range(21,25):
                                        tempval = look_buffer[x]
#                                        print('H'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[5].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[5].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[5].setText(str(gcvars.UltrasonicParmList[5].value))

                                    # Temperature
                                    gcvars.UltrasonicParmList[6].value = 0
                                    multiplier = 1
                                    for x in range(26,29):
                                        tempval = look_buffer[x]
#                                        print('T'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[6].value += bcdval*multiplier
                                        multiplier *= 100
                                    self.ui.parmbutton[6].setText(str(gcvars.UltrasonicParmList[6].value/100.0))


                                    # Checksum
                                    gcvars.UltrasonicParmList[7].value = look_buffer[30]
                                    self.ui.parmbutton[7].setText(str(format(gcvars.UltrasonicParmList[7].value,"02x")))

                                    gcvars.wait_reply_timer = 5                                            
                                        

                                else:
                                    self.ui.ReceiveMemo.appendPlainText("Checksum Failed "+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index])+" Expected {:X}".format(read_checksum))



    def parseReceive_fs000x(self):
        starttokenfound = False
        endtokenfound = False
        check_index = 0
        check_end_index = 0
        look_buffer = [0] * 256
        look_buffer_index = 0
        input_checksum = 0
        temp_substring = ""
        getindex = 0
        index = 0

        if(gcvars.read_index != gcvars.receive_index):
#                print('Read Index = {0}, Receive Index = {1}'.format(gcvars.read_index,gcvars.receive_index))
            check_index = gcvars.read_index
            starttokenfound = False
            while check_index != gcvars.receive_index and not starttokenfound:
                if gcvars.receive_buffer[check_index] != 0x42:
                    # discard characters that aren't start of message
                    check_index += 1
                    check_index &= 0xFF
                    gcvars.read_index += 1
                    gcvars.read_index &= 0xFF
                else:
                    # Got a potential message to parse
                    print('Got Start of Message')
                    starttokenfound = True
                    check_end_index = check_index
                    endtokenfound = False
                    while (check_end_index != gcvars.receive_index) and (not endtokenfound):
                        look_buffer[look_buffer_index] = gcvars.receive_buffer[check_end_index]
                        look_buffer_index += 1
                        if look_buffer_index > 32:
                            # overflow exit
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                            print('Overflow, length is ',look_buffer_index)
                        elif gcvars.receive_buffer[check_end_index] != 0x16 and look_buffer_index == 32:
                            print('Bad End Char ',gcvars.receive_buffer[check_end_index],' length is ',look_buffer_index)
                            print("".join(format(x,'02x') for x in look_buffer[0:look_buffer_index-1]))
                            endtokenfound = True
                            gcvars.read_index = gcvars.receive_index
                            check_end_index = gcvars.receive_index
                        elif look_buffer_index < 32:
#                                print('Adding Char ',ord(gcvars.receive_buffer[check_end_index]),' length is ',len(look_buffer))
                            check_end_index += 1
                            check_end_index &= 0xFF
                        else:
                            print('Got end of message')
                            
                            gcvars.read_index = check_end_index + 1
                            gcvars.read_index &= 0xFF
                            endtokenfound = True
                            if look_buffer_index > 4:
                                print("".join(format(x,'02x') for x in look_buffer[:32]))
                                checksum_valid = True
                                try:
                                    input_checksum = look_buffer[30]
                                    print('Input Checksum is ',input_checksum,' length is ',look_buffer_index)
                                except:
                                    self.ui.ReceiveMemo.appendPlainText('ERROR - input checksum invalid format '+look_buffer)
                                    checksum_valid = False
                                print(input_checksum)
                                read_checksum = 0
                                for index in range(2, look_buffer_index-3):
                                    read_checksum += look_buffer[index]
                                read_checksum &= 0xFF
                                print(read_checksum)
                                if(input_checksum == read_checksum):
                                    print("".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                                    self.ui.ReceiveMemo.appendPlainText('Received : '+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index]))
                                    gcvars.UltrasonicParmList[0].value = look_buffer[5]
                                    self.ui.parmbutton[0].setText(str(look_buffer[5]))

                                    # Device ID
                                    gcvars.UltrasonicParmList[0].value = 0
                                    for x in range(2,7):
                                        gcvars.UltrasonicParmList[0].value *= 256
                                        gcvars.UltrasonicParmList[0].value += look_buffer[x]
                                    self.ui.parmbutton[0].setText(str(format(gcvars.UltrasonicParmList[0].value,"08x")))

                                    # Version
                                    gcvars.UltrasonicParmList[1].value = look_buffer[7]
                                    self.ui.parmbutton[1].setText(str(look_buffer[7]))

                                    # Status Byte
                                    gcvars.UltrasonicParmList[2].value = look_buffer[29]
                                    self.ui.parmbutton[2].setText(str(format(gcvars.UltrasonicParmList[2].value,"02x")))


                                    # Acc. Flow
                                    gcvars.UltrasonicParmList[3].value = 0
                                    multiplier = 1
                                    for x in range(9,15):
                                        tempval = look_buffer[x]
#                                        print('A'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[3].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[3].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[3].setText(str(gcvars.UltrasonicParmList[3].value/1000.0))

                                    # Ins. Flow
                                    gcvars.UltrasonicParmList[4].value = 0
                                    multiplier = 1
                                    for x in range(16,20):
                                        tempval = look_buffer[x]
#                                        print('I'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[4].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[4].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[4].setText(str(gcvars.UltrasonicParmList[4].value/100.0))

                                    # Acc. Time
                                    gcvars.UltrasonicParmList[5].value = 0
                                    multiplier = 1
                                    for x in range(21,25):
                                        tempval = look_buffer[x]
#                                        print('H'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[5].value += bcdval*multiplier
                                        print(gcvars.UltrasonicParmList[5].value)
                                        multiplier *= 100
                                    self.ui.parmbutton[5].setText(str(gcvars.UltrasonicParmList[5].value))

                                    # Temperature
                                    gcvars.UltrasonicParmList[6].value = 0
                                    multiplier = 1
                                    for x in range(26,29):
                                        tempval = look_buffer[x]
#                                        print('T'+format(tempval,'02x'))
                                        bcdval = (tempval&0x0F) + (tempval >> 4)*10
                                        gcvars.UltrasonicParmList[6].value += bcdval*multiplier
                                        multiplier *= 100
                                    self.ui.parmbutton[6].setText(str(gcvars.UltrasonicParmList[6].value/100.0))


                                    # Checksum
                                    gcvars.UltrasonicParmList[7].value = look_buffer[30]
                                    self.ui.parmbutton[7].setText(str(format(gcvars.UltrasonicParmList[7].value,"02x")))

                                    gcvars.wait_reply_timer = 5                                            
                                        

                                else:
                                    self.ui.ReceiveMemo.appendPlainText("Checksum Failed "+"".join(format(x,'02x') for x in look_buffer[0:look_buffer_index])+" Expected {:X}".format(read_checksum))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    timer = QTimer()
    timer.timeout.connect(window.tick)
    timer.start(50)

    app.exec_()

if __name__ == "__main__":
    main()    
