from ..core.view import View
import sys
from ..core.style import Style

if sys.platform == "darwin":
    from Cocoa import NSView


class Column(View):
    def get_osx_render(self, parent=None, superview: NSView = None):
        parent: View = parent
        self.children.reverse()

        ns_view = NSView.alloc().initWithFrame_(((0, 0), (0, 0)))

        children_osx_renders = [child.get_osx_render(parent=self, superview=ns_view) for child in self.children]

        def max_width_key(key):
            return key.frame().size.width

        width = self.style.width if self.style.width is not None else max(children_osx_renders, key=max_width_key).frame().size.width
        height = 0

        for child_object in children_osx_renders:
            height += child_object.frame().size.height

        height += self.style.gap * (len(self.children) - 1) if self.style.gap is not None else 0

        ns_view_frame = ns_view.frame()
        ns_view_frame.size.height = height
        ns_view_frame.size.width = width

        for child_object in self.children:
            ns_child = child_object.get_osx_render(parent=self, superview=ns_view)
            child_frame = ns_child.frame()
            point_y = 0

            index = self.children.index(child_object)
            for i in range(index):
                point_y += self.children[i].get_osx_render(parent=self, superview=ns_view).frame().size.height

            point_y += self.style.gap * index
            child_frame.origin.y = point_y
            child_frame.origin.x = ns_view_frame.size.width / 2 - child_frame.size.width / 2

            ns_child.setFrame_(child_frame)
            ns_view.addSubview_(ns_child)

        ns_view.setFrame_(ns_view_frame)
        return ns_view