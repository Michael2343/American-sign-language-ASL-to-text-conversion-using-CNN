from PyQt5.QtWidgets import *
from PyQt5.uic import *
import socket
from CONST import *
import time
import threading

class ClientPage(QDialog):
    def __init__(self,widget):
        super(ClientPage,self).__init__()
        loadUi("ui/ClientPage.ui",self)
        self.widget = widget
                
        self.nameLabel.setPlaceholderText("Client name")
        self.ipLabel.setPlaceholderText("Host IP")
        self.portLabel.setPlaceholderText("Host port")

        self.errorLabel.setText("")

        self.nameLabel.setText("b")
        self.ipLabel.setText("192.168.56.1")
        self.portLabel.setText("1234")

        self.connectButton.clicked.connect(self.connect_client)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def error(self,error):   
        errorThread = threading.Thread(target=self.clean_error ,args=(error,))
        errorThread.start()
    
    def clean_error(self,error):
        self.errorLabel.setText(error)
        time.sleep(1)
        self.errorLabel.setText("")

    def connect_client(self):
        self.name = self.nameLabel.text()
        self.ip=self.ipLabel.text()
        self.port=self.portLabel.text()
        if self.name == "" or self.ip == "" or self.port == "" :
            self.error("Enter all fields!")
            return
        try:
            self.clientSocket.connect((self.ip, int(self.port)))
            self.widget.setCurrentIndex(CLIENT_CHAT_PAGE)
            clientChatWidget = self.widget.currentWidget()
            clientChatWidget.save_info(self.clientSocket,self.name)
        except Exception as e:
            if str(e)=="[Errno 111] Connection refused":
                self.error("Cannot connect")
