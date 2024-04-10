"""
# This script defines a PyQt5 dialog class for the chat page of the application.
# The chat page allows users to send and receive messages.
# It also integrates YOLOv5 and densenet121 for real-time object detection through the webcam.
"""

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
import collections 

# Resolving file paths and adding root directory to PATH
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# Defining a custom signal class for message communication between threads
class MessageSignal(QObject):
    message_received = pyqtSignal(str,str)

# Class defining the chat page dialog
class Chat(QDialog):
    def __init__(self,widget):
        super(Chat,self).__init__()
        loadUi("ui/Chat.ui",self)
        self.widget = widget
        
        # Connecting button click events to methods
        self.sendButton.clicked.connect(self.send_message)
        self.chatText.returnPressed.connect(self.send_message)
        
        self.translatorButton.clicked.connect(self.active_netowrk)
        # Hiding the camera feed by default
        self.cameraFeed.setVisible(False)
        self.scrollArea.setGeometry(130, 80, 961, 600)
        self.scrollAreaWidget.setGeometry(0, 0, 961-15, self.scrollAreaWidget.height())
        self.translatorButton.setStyleSheet("background-color : red") 
                
        # Initializing message signal for inter-thread communication
        self.message_signal = MessageSignal()
        self.message_signal.message_received.connect(self.add_new_message_to_box)
        self.active_network_flag = [False]    
        
        # Number of predictions to consider for determining message input
        self.last_predicts = 10
        self.letter_history = [" "]*self.last_predicts    
        
    # Method to set YOLOv5 instance
    def set_yolo(self,yolo):
        self.yolov5_instance = yolo
  
    # Method to save connection information
    def save_info(self,con,name):
        self.con =con
        self.name = name
        self.msgThread = threading.Thread(target=self.handle_msg, args=(self.con,))
        # Starting message handling thread
        self.msgThread.start()
     
    # Method to toggle network activity
    def active_netowrk(self):
        self.active_network_flag[0] = not self.active_network_flag[0]
        print(self.active_network_flag[0])
        if self.active_network_flag[0]:
            self.translatorButton.setStyleSheet("background-color : green") 
            self.cameraFeed.setVisible(True)
            self.scrollArea.setGeometry(680, 80, 490, 600)
            self.scrollAreaWidget.setGeometry(0, 0, 490-15, self.scrollAreaWidget.height())
            # Starting YOLOv5 object detection
            self.yolov5_instance.main(self.active_network_flag)

        else:
            self.translatorButton.setStyleSheet("background-color : red") 
            self.cameraFeed.setVisible(False)
            self.scrollArea.setGeometry(130, 80, 961, 600)
            self.scrollAreaWidget.setGeometry(0, 0, 961-15, self.scrollAreaWidget.height())

    # Method to add a new message to the chat box
    def add_new_message_to_box(self,message,color):
        label = QLabel(message)
        style = generate_style(color)
        label.setStyleSheet(style)  
        label.setWordWrap(True)  # Enable word wrapping
        self.vbox.addWidget(label)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum()+10)
        QApplication.processEvents()

    # Method to send a message
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

    # Method to handle incoming messages
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
    
    # Method to display webcam feed and process predictions
    def show_webcam(self,result):
        # Retrieving frame from YOLOv5 + densenet121 result
        frame = result["image"]

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        width = self.cameraFeed.width()
        height = self.cameraFeed.height()
        bytes_per_line = 3 * width
        pixmap = QPixmap(QImage(frame_rgb, width, height, bytes_per_line, QImage.Format_RGB888))
        # Display the QPixmap in the QLabel
        self.cameraFeed.setPixmap(pixmap)
        
        # Check if the prediction is valid
        valid = result["valid"]
        if valid:
            # Set focus on the QLineEdit to see the text cursor
            self.chatText.setFocus()
            
            label = result["label"]
            self.letter_history.append(label)
            if len(self.letter_history) > self.last_predicts:
                self.letter_history.pop(0)
            
            counter = collections.Counter(self.letter_history)

            # Find the label with the highest occurrence
            most_common_element, occurrences = counter.most_common(1)[0]
            percentage = (float(occurrences) / self.last_predicts) * 100

            # Check if the percentage of the most common label is within the specified range
            if 70<=percentage<=100 and most_common_element != " ":
                if most_common_element == "ENTER": 
                    self.send_message() # Trigger sending a message if "ENTER" is predicted
                elif most_common_element == "DELETE":
                    self.chatText.backspace() # Trigger backspacing if "DELETE" is predicted
                elif most_common_element == "SPACE":
                    self.chatText.setText((self.chatText.text() + " "))  # Add a space if "SPACE" is predicted
                else:                        
                    print("most_common_element:"+most_common_element)  
                    self.chatText.setText((self.chatText.text() + most_common_element)) # Print the most common label
                
                self.letter_history = [" "]*self.last_predicts
                