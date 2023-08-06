import builtins

from .view import View
from .style import Style
import sys

if sys.platform == "darwin":
    from Cocoa import NSView
    from Cocoa import NSButton


class Button(View):
    text: str
    onclick = None

    def __init__(self, text: str, style: Style=None, onclick=None):
        super().__init__(style=style)
        self.text = text
        self.onclick = onclick

    def get_osx_render(self, parent=None, superview: NSView = None):
        b = NSButton.alloc().initWithFrame_(((0, 0), (0, 0)))
        b.setBezelStyle_(4)
        b.setTitle_(self.text)
        b.sizeToFit()

        btn_frame = b.frame()
        btn_frame.size.width = self.style.width if self.style.width is not None else btn_frame.size.width
        btn_frame.size.height = self.style.height if self.style.height is not None else btn_frame.size.height
        b.setFrame_(btn_frame)

        return b
