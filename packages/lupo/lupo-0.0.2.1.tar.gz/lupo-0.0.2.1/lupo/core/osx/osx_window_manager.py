from Cocoa import NSWindow, NSObject, NSApp, NSApplication, NSMenu, NSMenuItem
from PyObjCTools import AppHelper
from .osx_display import get_display_size


class OSX_OBJC_WINDOW:
    title = ""
    window_x = 0
    window_y = 0
    window_width = 250
    window_height = 250

    def __init__(self):
        self.win = NSWindow.alloc()

        screen_size = get_display_size()

        frame = (
            (screen_size["width"] / 2 - self.window_width / 2, screen_size["height"] / 2 - self.window_height / 2),
            (self.window_width, self.window_height)
        )

        self.win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
        self.win.setTitle_(self.title)
        self.win.setLevel_(3)

    def set_title(self, title):
        self.title = title
        self.win.setTitle_(self.title)

    def set_body(self, osx_render):
        self.win.contentView().addSubview_(osx_render)

    def set_size(self, width, height):
        self.window_width = width
        self.window_height = height

        frame = self.win.frame()
        frame.size.width = width
        frame.size.height = height

        self.win.setContentSize_(frame.size)

    def display_window(self):
        self.win.display()
        self.win.orderFrontRegardless()
        AppHelper.runEventLoop()
