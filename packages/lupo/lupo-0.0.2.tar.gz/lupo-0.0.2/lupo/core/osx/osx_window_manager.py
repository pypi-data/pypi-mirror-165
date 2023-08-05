from Cocoa import NSObject, NSApplication, NSApp, NSWindow, NSButton, NSSound
from PyObjCTools import AppHelper


class OSX_OBJC_WINDOW:
    title = ""
    window_x = 0
    window_y = 0
    window_width = 250
    window_height = 250

    def __init__(self):
        self.win = NSWindow.alloc()
        frame = ((self.window_x, self.window_y), (self.window_width, self.window_height))

        self.win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
        self.win.setTitle_(self.title)
        self.win.setLevel_(3)

    def set_title(self, title):
        self.title = title
        self.win.setTitle_(self.title)

    def display_window(self):
        self.win.display()
        self.win.orderFrontRegardless()
        AppHelper.runEventLoop()