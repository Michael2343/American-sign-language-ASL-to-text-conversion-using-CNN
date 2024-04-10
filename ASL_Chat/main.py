"""
This script serves as the main entry point for the application.
It sets up the Qt application, creates window widgets, loads pages,
and initializes neural network models. It also establishes connections
between different components of the application.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from CONST import *
from pages.HomePage import *
from pages.HostPage import *
from pages.ClientPage import *
from pages.Chat import *
from yolov5.YOLOv5 import YOLOv5
from densenet import *
from PIL import Image
import torch

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Creating a stacked widget to manage multiple pages/windows
    widgetList = QStackedWidget()
    
    # Adding instances of all window widgets (pages) to the stacked widget
    widgetList.addWidget(HomePage(widgetList))
    widgetList.addWidget(HostPage(widgetList))
    widgetList.addWidget(ClientPage(widgetList))
    chat = Chat(widgetList)
    widgetList.addWidget(chat)
    
    # Instantiating YOLOv5 and DenseNet models
    yolo = YOLOv5()
    densnet = make_densenet(type=DENSENET_TYPE).to(DEVICE)
    trained_model = torch.load(PT_PATH+PT_FILE)
    densnet.load_state_dict(trained_model.state_dict())#(type=DENSENET_TYPE).to(DEVICE)``
    
    # Connecting components between chat page, YOLOv5, and DenseNet for seamless integration
    yolo.set_densenet(densnet)
    yolo.set_window(chat)
    chat.set_yolo(yolo)
    
    # Setting window size and position on the screen
    initial_width = 1200
    initial_height = 800
    screen_rect = QApplication.desktop().availableGeometry()
    center_x = screen_rect.center().x() - initial_width //2
    center_y = screen_rect.center().y() - initial_height // 2
    widgetList.setGeometry(center_x, center_y, initial_width, initial_height)

    # Running the application
    try:
        widgetList.show()
        app.exec_()
    except Exception as e:
        print("Exception:",str(e))
        