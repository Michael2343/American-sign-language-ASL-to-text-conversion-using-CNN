# Constants
PORT = 1234
HOME_PAGE = 0
HOST_PAGE = 1
CLIENT_PAGE = 2
HOST_CHAT_PAGE = 3
CLIENT_CHAT_PAGE = 4

#Font
BASE_STYLE = (
    f'font-weight: bold; '
    f'font-style: italic; '
    f'font-family: halvetica; '
    f'font-size: 16px; '
    f'padding: 5px; '
    f'border-radius: 10px; '
    f'width: 425px;'
)

def generate_style(color):
    return BASE_STYLE + (
    f'color: {color}; '
    f'border: 1px solid {color}; '
    )
