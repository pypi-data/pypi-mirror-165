import os
import platform
from .osx.osx_window_manager import OSX_OBJC_WINDOW

class Window:
    __title = "Lupo Window"

    def __init__(self):
        ...

    def open_window(self):
        if platform.system() == "Darwin":
            osx_window = OSX_OBJC_WINDOW()
            osx_window.set_title(self.__title)
            osx_window.display_window()