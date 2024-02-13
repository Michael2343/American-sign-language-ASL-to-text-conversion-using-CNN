from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import threading
from CONST import *
import cv2
import time
import torch
import numpy as np
from pathlib import Path
import sys
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

class MessageSignal(QObject):
    message_received = pyqtSignal(str,str)

class Chat(QDialog):
    def __init__(self,widget):
        super(Chat,self).__init__()
        loadUi("ui/Chat.ui",self)
        self.widget = widget
        self.sendButton.clicked.connect(self.send_message)
        self.chatText.returnPressed.connect(self.send_message)
        self.translatorButton.clicked.connect(self.active_netowrk)
        self.cameraFeed.setVisible(False)
        self.scrollArea.setGeometry(130, 80, 961, 600)
        self.scrollAreaWidget.setGeometry(0, 0, 961-15, self.scrollAreaWidget.height())

        self.translatorButton.setStyleSheet("background-color : red") 
        
        self.message_signal = MessageSignal()
        self.message_signal.message_received.connect(self.add_new_message_to_box)
        self.active_network_flag = [False]        
        
    def set_yolo(self,yolo):
        self.yolov5_instance = yolo
        
    def save_info(self,con,name):
        self.con =con
        self.name = name
        self.msgThread = threading.Thread(target=self.handle_msg, args=(self.con,))
        self.msgThread.start()
     
    def active_netowrk(self):
        self.active_network_flag[0] = not self.active_network_flag[0]
        print(self.active_network_flag[0])
        if self.active_network_flag[0]:
            self.translatorButton.setStyleSheet("background-color : green") 
            self.cameraFeed.setVisible(True)
            self.scrollArea.setGeometry(680, 80, 490, 600)
            self.scrollAreaWidget.setGeometry(0, 0, 490-15, self.scrollAreaWidget.height())
            self.yolov5_instance.main(self.active_network_flag)

        else:
            self.translatorButton.setStyleSheet("background-color : red") 
            self.cameraFeed.setVisible(False)
            self.scrollArea.setGeometry(130, 80, 961, 600)
            self.scrollAreaWidget.setGeometry(0, 0, 961-15, self.scrollAreaWidget.height())

    def add_new_message_to_box(self,message,color):
        label = QLabel(message)
        style = generate_style(color)
        label.setStyleSheet(style)  
        label.setWordWrap(True)  # Enable word wrapping
        self.vbox.addWidget(label)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum()+10)
        QApplication.processEvents()

    def send_message(self):
        message = self.chatText.text()
        if message.strip() == '':
            return
        self.chatText.setText("")

        my_message = "You: " + message
        self.add_new_message_to_box(my_message,"red")

        send_message = self.name + ": " +message
        self.con.send(send_message.encode('utf-8'))
        print("SEND: " + message)

    def handle_msg(self,con):
        while True:
            try:
                message = con.recv(1024).decode('utf-8')
                print("GOT: "+message)
                self.message_signal.message_received.emit(message,"green")
            except:
                self.con.close()
                print("Connection closed!")
                break
    
    def show_webcam(self,result):
        frame = result["image"]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        width = self.cameraFeed.width()
        height = self.cameraFeed.height()
        bytes_per_line = 3 * width
        
        pixmap = QPixmap(QImage(frame_rgb, width, height, bytes_per_line, QImage.Format_RGB888))
        # Display the QPixmap in the QLabel
        
        self.cameraFeed.setPixmap(pixmap)
