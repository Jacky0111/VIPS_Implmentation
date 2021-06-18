class SeparatorVO:
    TYPE_HORIZONTAL = 1
    TYPE_VERTICAL = 2

    x = 0
    y = 0
    width = 0
    height = 0
    typ = 0
    weight = 7

    one_side = None
    another_side = None

    def __init__(self, x, y, width, height, typ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.typ = typ

    def __gt__(self, other):
        return self.weight > other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def equals(self, obj):
        if isinstance(obj, SeparatorVO):
            if obj.typ == SeparatorVO.TYPE_VERTICAL:
                if obj.x == self.x and obj.width == self.width:
                    return True
        return self == obj
