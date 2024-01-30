from PyQt5.QtWidgets import *
from PyQt5.uic import *
from CONST import *

class HomePage(QDialog):
    def __init__(self,widget):
        super(HomePage,self).__init__()
        loadUi("ui/HomePage.ui",self)
        self.widget = widget
        self.hostButton.clicked.connect(self.go_to_host_page)
        self.clientButton.clicked.connect(self.go_to_client_page)

    def go_to_host_page(self):
        self.widget.setCurrentIndex(HOST_PAGE)

    def go_to_client_page(self):
        self.widget.setCurrentIndex(CLIENT_PAGE)
