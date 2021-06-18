class CssBox:
    __slots__ = ('attributes', 'bounds', 'bgColor', 'display', 'fontSize', 'fontWeight', 'visibility')

    def __init__(self, attributes, bounds, bgColor, display, fontSize, fontWeight, visibility):
        self.attributes = attributes
        self.bounds = bounds
        self.bgColor = bgColor
        self.display = display
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.visibility = visibility
