from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import threading
from CONST import *
import cv2
import time

class MessageSignal(QObject):
    message_received = pyqtSignal(str,str)

class Chat(QDialog):
    def __init__(self,widget,type):
        super(Chat,self).__init__()
        loadUi("ui/Chat.ui",self)
        self.widget = widget
        self.type = type # asl / non-asl
        self.sendButton.clicked.connect(self.send_message)
        self.chatText.returnPressed.connect(self.send_message)
        self.translatorButton.clicked.connect(self.active_netowrk)
        self.cameraFeed.setVisible(False)
        self.scrollArea.setGeometry(130, 80, 961, 600)
        self.scrollAreaWidget.setGeometry(0, 0, 961-15, self.scrollAreaWidget.height())

        self.translatorButton.setStyleSheet("background-color : red") 
        
        self.message_signal = MessageSignal()
        self.message_signal.message_received.connect(self.add_new_message_to_box)
        self.active_network_flag = False

    def save_info(self,con,name):
        self.con =con
        self.name = name
        self.msgThread = threading.Thread(target=self.handle_msg, args=(self.con,))
        self.msgThread.start()

    def active_netowrk(self):
        self.active_network_flag = not self.active_network_flag
        print(self.active_network_flag)
        if self.active_network_flag:
            self.camThread = threading.Thread(target=self.show_webcam)
            self.camThread.start()
            self.translatorButton.setStyleSheet("background-color : green") 
            self.cameraFeed.setVisible(True)
            self.scrollArea.setGeometry(680, 80, 490, 600)
            self.scrollAreaWidget.setGeometry(0, 0, 490-15, self.scrollAreaWidget.height())
        else:
            self.translatorButton.setStyleSheet("background-color : red") 
            self.cameraFeed.setVisible(False)
            self.camThread.join()
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
    
    def show_webcam(self):
        self.cam = cv2.VideoCapture(0)
        labelWidth = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        labelHeight = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(labelWidth,labelHeight)
        self.cameraFeed.setFixedWidth(labelWidth)
        self.cameraFeed.setFixedHeight(labelHeight)
        while self.active_network_flag:
            ret_val, frame = self.cam.read()
            frame = cv2.resize(frame, (labelWidth, labelHeight))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            pixmap = QPixmap(QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888))
            # Display the QPixmap in the QLabel
            self.cameraFeed.setPixmap(pixmap)
            time.sleep(0.04)
        self.cam.release()
