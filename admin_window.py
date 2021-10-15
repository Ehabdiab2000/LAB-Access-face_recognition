
import sqlite3

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage, QPixmap ,QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QApplication, QMainWindow ,QInputDialog, QLineEdit
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import time
import sys
#from out_window import Ui_OutputDialog

class Ui_Admin_Dialog(QDialog):
    def __init__(self):
        super(Ui_Admin_Dialog, self).__init__()
        loadUi("./adminwindow.ui", self)

        #Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        self.capture = cv2.VideoCapture(0)
        self.buttonHandle()
        self.image = None
        self.img =None
        self.timer = QTimer(self)  # Create Timer
    def buttonHandle(self):
        self.RegisterBtn.clicked.connect(self.registerUser)
        self.load.clicked.connect(self.loadLog)

        self.pushButton.clicked.connect(self.startReg)
    def startReg(self):
        self.timer.timeout.connect(self.displayImage2)  # Connect timeout to the output function
        self.timer.start(50)  # emit the timeout() signal at x=10ms


    def loadLog(self):
        format = "yyyy MM dd hh mm ss";
        #print(self.fromTime.dateTime().toString(format))
        db = sqlite3.connect('faceAccess.db')
        cursor = db
        command = '''SELECT * FROM log WHERE time BETWEEN ? AND ? ORDER BY time DESC'''
        row= (self.fromTime.dateTime().toString(format),self.toTime.dateTime().toString(format))
        result = cursor.execute(command,row)

        ### to Fill table with result
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if(column_number==2):
                    item=self.getImageLable(data)
                    self.table.setCellWidget(row_number,column_number,item)
                else :
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.table.verticalHeader().setDefaultSectionSize(80)

    def getImageLable(self,imName):
        imageLabel =QtWidgets.QLabel(self.log)
        #imageLabel.setText("aa")
        imageLabel.setScaledContents(True)
        #pixmap = QtGui.QPixmap("2020 11 16 17 26 04.jpg")
        imagename =str("photos\{0}.jpg".format(str(imName)))
        #print(imagename)

        pixmap = QtGui.QPixmap(str("photos\{0}.jpg".format(imName)))

        #pixmap.loadFromData(image,'jpg')
        imageLabel.setPixmap(pixmap)
        return imageLabel


    def registerUser(self):

        db = sqlite3.connect('faceAccess.db')
        cursor = db.cursor()

        name_ = self.regName.text()
        cardNo_= self.cardNo.text()
        cv2.imwrite("users\{0}.jpg".format(name_), self.img)
        row = (name_,cardNo_)
        command = '''REPLACE INTO users (name,cardNo) VALUES (?,?)'''
        cursor.execute(command, row)
        db.commit()

        cur_img = cv2.imread("users\{0}.jpg".format(name_))

        #Ui_OutputDialog.class_names.append(name_)

        # get encoding for the new user image


        img = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)  ## convert color
        boxes = face_recognition.face_locations(img)  # get face location
        encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]  # get the encoding for the detected face
        # encode = face_recognition.face_encodings(img)[0]
        #Ui_OutputDialog.encode_list.append(encodes_cur_frame)
        #Ui_OutputDialog.timer.stop()

    def getUserPassword(self, text):
        db = sqlite3.connect('faceAccess.db')
        cursor = db.cursor()
        command = '''SELECT PassCode FROM users WHERE name=? '''
        result = cursor.execute(command, [text]).fetchone()
        #if result:
        password = result[0]
        return password

    def getInputPassword(self):
        text, okPressed = QInputDialog.getText(self, "Get PIN", "Enter Your PIN:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text


    def stopTimer(self):
        self.timer.stop()
        print('timer stopped')

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names)

    def displayImage2(self):
        ret, self.image = self.capture.read()
        image = cv2.resize(self.image, (640, 480))
        self.img = image.copy()

        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
         if image.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
         else:
            qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.imgLabel2.setPixmap(QPixmap.fromImage(outImage))
        self.imgLabel2.setScaledContents(True)

    def closeEvent(self, event):
        print("closing PyQtTest")
        self.timer.stop()
        # report_session()