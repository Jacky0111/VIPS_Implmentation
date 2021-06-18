#  4.1 Visual Block Extraction

from VariationOrder.BlockVO import BlockVO
from Rule.BlockRule import BlockRule


class VisualBlockExtraction:
    block = None
    hr_list = []
    block_list = []
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 1

    def __init__(self):
        self.block = BlockVO()
        self.hrList = []
        self.block_list = []

    def service(self, nodeList):
        BlockRule.initialization(nodeList)
        body = nodeList[0]
        block_vo = BlockVO()
        self.initializeBlock(body, self.block)
        print('-----Initialization Completed-----')
        count4 = 0
        self.divideBlock(self.block)
        print(self.count3)
        print("-----Division Completed-----")
        block_vo.refreshBlock(self.block)
        print("-----Refreshing Completed-----")
        self.fillList(self.block)
        print("-----Filling Completed-----")
        # self.checkText()
        return self.block

    # TO BE IMPROVED
    def initializeBlock(self, given_box, given_block):
        given_block.boxes.append(given_box)
        print(self.count1, "####Here Name=", given_box.nodeName)
        self.count1 += 1
        print(self.count4)
        if given_box.nodeName == 'hr':
            self.hrList.append(given_block)
            self.count2 = 0
        if given_box.nodeType != 3:
            subBoxList = given_box.childNodes
            for b in subBoxList:
                if b.nodeName != "script" and b.nodeName != "noscript" and b.nodeName != "style":
                    self.count2 += 1
                    print(self.count2)
                    block_vo = BlockVO()
                    block_vo.parent = given_block
                    given_block.children.append(block_vo)
                    self.initializeBlock(b, block_vo)

    def divideBlock(self, given_block):
        self.count3 += 1
        print(self.count3)
        if given_block.isDividable and BlockRule.dividable(given_block):
            given_block.isVisualBlock = False
            for b in given_block.children:
                self.count4 += 1
                print(self.count4)
                self.divideBlock(b)

    def fillList(self, given_block):
        if given_block.isVisualBlock:
            self.block_list.append(given_block)
        else:
            for b in given_block.children:
                self.fillList(b)

    # TO BE IMPROVED
    def checkText(self):
        pass
