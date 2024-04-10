"""
This script defines a PyQt5 dialog class for the client page of the application.
The client page allows the user to connect to a host server.
It includes methods to handle client connection, error handling, and navigation to the chat page.
"""

from PyQt5.QtWidgets import *
from PyQt5.uic import *
import socket
from CONST import *
import time
import threading

# Class defining the client page dialog
class ClientPage(QDialog):
    def __init__(self,widget):
        super(ClientPage,self).__init__()
        loadUi("ui/ClientPage.ui",self)
        self.widget = widget
                
        self.nameLabel.setPlaceholderText("Client name")
        self.ipLabel.setPlaceholderText("Host IP")
        self.portLabel.setPlaceholderText("Host port")

        self.errorLabel.setText("")

        # Setting default values for input fields (for testing)
        self.nameLabel.setText("")
        self.ipLabel.setText("192.168.56.1")
        self.portLabel.setText("1234")

        self.connectButton.clicked.connect(self.connect_client)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Method to display error message
    def error(self,error):   
        errorThread = threading.Thread(target=self.clean_error ,args=(error,))
        errorThread.start()
    
    # Method to clear error message after a delay
    def clean_error(self,error):
        self.errorLabel.setText(error)
        time.sleep(1)
        self.errorLabel.setText("")

    # Method to connect client to the server
    def connect_client(self):
        self.name = self.nameLabel.text()
        self.ip=self.ipLabel.text()
        self.port=self.portLabel.text()
        # Validating input fields
        if self.name == "" or self.ip == "" or self.port == "" :
            self.error("Enter all fields!")
            return
        try:
            # Attempting to connect to the server
            print("MAKE chat for client")
            self.clientSocket.connect((self.ip, int(self.port)))
            self.widget.setCurrentIndex(CHAT_PAGE)
            clientChatWidget = self.widget.currentWidget()
            clientChatWidget.save_info(self.clientSocket,self.name)
        except Exception as e:
            if str(e)=="[Errno 111] Connection refused":
                self.error("Cannot connect")
