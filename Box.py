import rectangle


class Box:
    isBlock = None
    isEmpty = None
    displayed = None
    visible = None

    def __init__(self):
        self.isBlock = False
        self.isEmpty = False
        self.displayed = True
        self.visible = True

    def isBlock(self):
        return self.isBlock

    def isEmpty(self):
        return self.isEmpty

    def isDisplayed(self):
        return self.displayed

    def isVisible(self):
        return self.visible
