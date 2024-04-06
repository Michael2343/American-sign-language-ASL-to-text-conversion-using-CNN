import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from CONST import *
from pages.HomePage import *
from pages.HostPage import *
from pages.ClientPage import *
# from pages.prev.HostChatPage import *
# from pages.prev.ClientChatPage import *
# from pages.prev.ChatPage import *
from pages.Chat import *
from yolov5.YOLOv5 import YOLOv5
from densenet import *
from PIL import Image
import torch

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widgetList = QStackedWidget()
    widgetList.addWidget(HomePage(widgetList))

    widgetList.addWidget(HostPage(widgetList))
    widgetList.addWidget(ClientPage(widgetList))
    
    # widgetList.addWidget(HostChatPage(widgetList))
    # widgetList.addWidget(ClientChatPage(widgetList))

    # widgetList.addWidget(ChatPage(widgetList,"host"))
    # widgetList.addWidget(ChatPage(widgetList,"client"))

    chat = Chat(widgetList)
    widgetList.addWidget(chat)
    
    yolo = YOLOv5()
    
    densnet = make_densenet(type=DENSENET_TYPE).to(DEVICE)
    # FILE = Path(__file__).resolve()
    # ROOT = FILE.parents[0]
    # print(ROOT)
    # x=os.open(PT_PATH+PT_FILE,os.O_RDONLY)
    # os.read(x,50)
    trained_model = torch.load(PT_PATH+PT_FILE)
    densnet.load_state_dict(trained_model.state_dict())#(type=DENSENET_TYPE).to(DEVICE)``
    
    yolo.set_densenet(densnet)
    yolo.set_window(chat)
    chat.set_yolo(yolo)
    
    # 1
    # widgetList.setFixedWidth(1200)
    # widgetList.setFixedHeight(800)

    # 2
    # widgetList.showFullScreen()  # Set the widget to show in full screen
    

    # 3
    # screen_rect = QApplication.desktop().availableGeometry()
    # widgetList.setGeometry(screen_rect)

    # 4
    initial_width = 1200
    initial_height = 800
    screen_rect = QApplication.desktop().availableGeometry()
    center_x = screen_rect.center().x() - initial_width //2
    center_y = screen_rect.center().y() - initial_height // 2
    widgetList.setGeometry(center_x, center_y, initial_width, initial_height)

    try:
        widgetList.show()
        app.exec_()
    except Exception as e:
        print("Exception:",str(e))
        