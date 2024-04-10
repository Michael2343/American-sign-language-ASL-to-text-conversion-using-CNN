"""
This script defines a PyQt5 dialog class for the host page of the application.
The host page allows the user to set up a server for communication.
It includes methods to handle starting the server, error handling, and connecting to clients.
"""

from PyQt5.QtWidgets import *
from PyQt5.uic import *
import socket
import threading
from CONST import *
import time

# Class defining the host page dialog
class HostPage(QDialog):
    def __init__(self,widget):
        super(HostPage,self).__init__()
        loadUi("ui/HostPage.ui",self)
        self.widget = widget
        self.nameLabel.setPlaceholderText("Host name")
        self.errorLabel.setText("")
        self.waitLabel.setText("")
        self.ipText.setText("")
        self.ip = socket.gethostbyname(socket.gethostname())
        self.openConButton.clicked.connect(self.start_con)

    # Method to start server connection
    def start_con(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.ip, PORT))       
            self.openServerThread = threading.Thread(target=self.start_server)
            self.openServerThread.start()
        except Exception as e:
            if str(e)=="[Errno 98] Address already in use":
                self.error("Address already in use!")

    # Method to display error message
    def error(self,error):   
        errorThread = threading.Thread(target=self.clean_error ,args=(error,))
        errorThread.start()
    
    # Method to clear error message after a delay
    def clean_error(self,error):
        self.errorLabel.setText(error)
        time.sleep(1)
        self.errorLabel.setText("")
        
    # Method to start the server for communication
    def start_server(self):
        self.name = self.nameLabel.text()
        if self.name == "":
            self.error("Enter name!")
            return
        try:
            self.waitLabel.setText("Wait for connection...")
            self.ipText.setText("IP {} | Port {}".format(self.ip, PORT))
            self.serverSocket.listen(1)
            print("Server is listening on {}:{}".format(self.ip, PORT))
            serverCon, addr = self.serverSocket.accept()
            self.serverCon = serverCon
            print("Client connected!")
            self.widget.setCurrentIndex(CHAT_PAGE)
            HostChatWidget = self.widget.currentWidget()
            HostChatWidget.save_info(self.serverCon,self.name)
        except Exception as e:
            self.error("Error connection!")
