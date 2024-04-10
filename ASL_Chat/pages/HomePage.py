"""
This script defines a PyQt5 dialog class for the home page of an application.
The home page contains buttons to navigate to different pages.
The script uses Qt Widgets and loads UI from a UI file using PyQt5's loadUi function.
It also includes methods to handle button clicks and navigate to other pages.
"""

from PyQt5.QtWidgets import *
from PyQt5.uic import *
from CONST import *

# Class defining the home page dialog
class HomePage(QDialog):
    def __init__(self,widget):
        super(HomePage,self).__init__()
        loadUi("ui/HomePage.ui",self)
        self.widget = widget
        # Connect button click events to corresponding methods
        self.hostButton.clicked.connect(self.go_to_host_page)
        self.clientButton.clicked.connect(self.go_to_client_page)
    
    # Method to navigate to the host page
    def go_to_host_page(self):
        self.widget.setCurrentIndex(HOST_PAGE)
    
    # Method to navigate to the client page
    def go_to_client_page(self):
        self.widget.setCurrentIndex(CLIENT_PAGE)
