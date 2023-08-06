import os
from .osx.osx_window_manager import OSX_OBJC_WINDOW
from .view import View
import sys


class Window:
    __title = "Lupo Window"
    body = View()
    __size = (300, 300)

    def __init__(self):
        if sys.platform == "darwin":
            self.osx_window = OSX_OBJC_WINDOW()

    def set_size(self, width: int, height: int):
        self.__size = (width, height)
        if sys.platform == "darwin":
            self.osx_window.set_size(self.__size[0], self.__size[1])

    def get_size(self):
        return self.__size

    def set_title(self, title: str):
        self.__title = title

        if sys.platform == "darwin":
            self.osx_window.set_title(self.__title)

    def open(self):
        if sys.platform == "darwin":
            self.body.style.width = self.__size[0]
            self.body.style.height = self.__size[1]
            self.osx_window.set_body(self.body.get_osx_render(superview=self.osx_window.win.contentView()))
            self.osx_window.set_title(self.__title)
            self.osx_window.display_window()