#  4.1 Visual Block Extraction
import time

from Rule.BlockRule import BlockRule


class VisualBlockExtraction:
    x = 0  # Separator coordinate x
    y = 0  # Separator coordinate y
    width = 0   # Separator width
    height = 0  # Separator height
    DoC = 0  # Degree of Coherence
    count = 1     # Counter of identity
    identity = 1  # ID

    parent = None  # Parent node
    isVisualBlock = True
    isDividable = True
    block = None

    boxes = []
    children = []
    block_list = []
    hr_list = []

    '''
    Considering python does not open for more than 1 constructor in one class. Therefore, I use the "choice" to identify.
    '''
    def __init__(self, choice=True):
        if choice:
            self.block = VisualBlockExtraction(False)
            self.hr_list = []
            self.block_list = []
        else:
            self.identity = str(VisualBlockExtraction.count)
            VisualBlockExtraction.count += 1
            self.boxes = []
            self.children = []

    '''
    Execution function
    Aim at finding all appropriate visual blocks contained in the current sub-page
    @param node_list
    @return block
    '''
    def runner(self, node_list):
        body = node_list[0]
        # Initialize Block
        print('---------------------------------------Initialize Block---------------------------------------')
        self.initializeBlock(body, self.block)
        # Divide Block
        print('-----------------------------------------Divide Block-----------------------------------------')
        self.divideBlock(self.block)
        # Refresh and Update Block
        print('-----------------------------------Refresh and Update Block-----------------------------------')
        self.refresh(self.block)
        # Fill Pool
        print('------------------------------------------Fill Pool-------------------------------------------')
        self.fillPool(self.block)
        return self.block

    '''
    Initialize the block with DOM nodes (Recursive Function)
    @param box
    @param block
    '''
    def initializeBlock(self, box, block):
        block.boxes.append(box)
        print(f'Node Name = {box.nodeName}')

        # For separator weight purpose
        if box.nodeName == 'hr':
            self.hr_list.append(box)

        if box.nodeType != 3:
            for b in box.childNodes:
                if box.nodeName != "script" and box.nodeName != "noscript" and box.nodeName != "style":
                    vbe = VisualBlockExtraction(False)
                    vbe.parent = block
                    block.children.append(vbe)
                    self.initializeBlock(b, vbe)

    '''
    Divide the block based on the heuristic rules (Recursive Function)
    @param block
    '''
    def divideBlock(self, block):
        if block.isDividable and BlockRule.dividable(block):
            block.isVisualBlock = False
            for b_child in block.children:
                self.divideBlock(b_child)

    '''
    Update the coordinate, width, height and visual cues of the block
    '''
    def updateBlock(self):
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print(f'id: {self.identity}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, DoC: {self.DoC},')
        for i in range(len(self.boxes)):
            # print(f'x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, DoC: {self.DoC},')
            # print()

            box = self.boxes[i]
            # print(f"box.visual_cues['bounds']['x']: {box.visual_cues['bounds']['x']}")
            # print(f"box.visual_cues['bounds']['y']: {box.visual_cues['bounds']['y']}")
            # print(f"box.visual_cues['bounds']['width']: {box.visual_cues['bounds']['width']}")
            # print(f"box.visual_cues['bounds']['height']: {box.visual_cues['bounds']['height']}")
            # print()

            if i == 0:
                self.x = box.visual_cues['bounds']['x']
                self.y = box.visual_cues['bounds']['y']
                self.width = box.visual_cues['bounds']['width']
                self.height = box.visual_cues['bounds']['height']
            else:
                x_width = self.x + self.width
                y_height = self.y + self.height
                box_x_width = box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width']
                box_y_height = box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height']
                x_width = box_x_width if (x_width < box_x_width) else x_width
                y_height = box_y_height if (y_height < box_y_height) else y_height
                self.x = box.visual_cues['bounds']['x'] if (box.visual_cues['bounds']['x'] < self.x) else self.x
                self.y = box.visual_cues['bounds']['y'] if (box.visual_cues['bounds']['y'] < self.y) else self.y
                self.width = x_width - self.x
                self.height = y_height - self.y
        #     print(f'id: {self.identity}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, DoC: {self.DoC},')
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    '''
    Refresh all of the blocks to ensure that all have been updated (Recursive Function)
    @param block
    '''
    @staticmethod
    def refresh(block):
        block.updateBlock()
        for child in block.children:
            VisualBlockExtraction.refresh(child)

    '''
    Fill the updated block into the pool (Recursive Function)
    @param block
    '''
    def fillPool(self, block):
        if block.isVisualBlock:
            self.block_list.append(block)
        else:
            for child in block.children:
                self.fillPool(child)

    def __str__(self):
        return f'id: {self.identity}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, ' \
               f'DoC: {self.DoC}, isVisualBlock: {self.isVisualBlock}, isDividable: {self.isDividable}'
