from AppKit import NSScreen


def get_display_size():
    ns_screen_size = NSScreen.mainScreen().frame().size

    return {
        "width": ns_screen_size.width,
        "height": ns_screen_size.height
    }

def set_menu_bar():
    ...