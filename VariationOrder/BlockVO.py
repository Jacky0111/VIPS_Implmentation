class BlockVO:
    x = 0
    y = 0
    width = 0
    height = 0
    DoC = 0  # Degree of Coherence
    count = 1

    identity = None
    boxes = []
    parent = None
    children = []
    isVisualBlock = True
    isDividable = True

    def __init__(self):
        self.identity = str(BlockVO.count)
        BlockVO.count += 1
        self.boxes = []
        self.children = []

    def refresh(self):
        for i in range(len(self.boxes)):
            box = self.boxes[i]
            if i == 0:
                self.x = box.visual_cues['bounds']['x']
                self.y = box.visual_cues['bounds']['y']
                self.width = box.visual_cues['bounds']['width']
                self.height = box.visual_cues['bounds']['height']
            else:
                rbx = self.x + self.width
                rby = self.y + self.height
                box_rbx = box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width']
                box_rby = box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height']
                rbx = box_rbx if (box_rbx > rbx) else rbx
                rby = box_rby if (box_rby > rby) else rby
                self.x = box.visual_cues['bounds']['x'] if (box.visual_cues['bounds']['x'] < self.x) else self.x
                self.y = box.visual_cues['bounds']['y'] if (box.visual_cues['bounds']['y'] < self.y) else self.y
                self.width = rbx - self.x
                self.height = rby - self.y

    @staticmethod
    def refreshBlock(block):
        block.refresh()
        for i in block.children:
            BlockVO.refreshBlock(i)

    def __str__(self):
        return f'Visual Block: {self.isVisualBlock}\n Children: {self.children}'
