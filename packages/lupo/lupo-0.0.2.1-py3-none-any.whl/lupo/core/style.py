class px(int):  # px type from CSS but instead of writing 100px you use px(100)
    value: int

    def __init__(self, number):
        self.value = number

    def __int__(self) -> int:
        return self.value


# TODO: More CSS Measurement Scales for Python


class Style:
    width: int = None
    height: int = None
    gap: int = None

    def __init__(
            self,
            width: int = None,
            height: int = None,
            gap: int = None
    ):
        # Assign the Values to class if assigned at init

        self.width = width if not None else self.width
        self.height = height if not None else self.height
        self.gap = gap if not None else self.gap
