from PyQt5.QtWidgets import *
from PyQt5.uic import *
import socket
import threading
from CONST import *
import time

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

    def error(self,error):   
        errorThread = threading.Thread(target=self.clean_error ,args=(error,))
        errorThread.start()
    
    def clean_error(self,error):
        self.errorLabel.setText(error)
        time.sleep(1)
        self.errorLabel.setText("")

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
