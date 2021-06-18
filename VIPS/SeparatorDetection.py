# 4.2 Visual Separator Detection
# 4.2.1 Separator Detection

from Rule.SeparatorRule import SeparatorRule
from VariationOrder.SeparatorVO import SeparatorVO


class SeparatorDetection:
    width = 0
    height = 0
    typ = 0
    separator_list = None
    count = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.separator_list = []

    def service(self, blocks, sep_type):
        pass

    '''
    Step 1
    Initialize the separator list. The list starts with only one separator (Pbe, Pee) whose start pixel and end pixel 
    are corresponding to the borders of the pool.
    '''

    def step1(self):
        pass

    '''
    Step 2
    For every block in the pool, the relation of the block with each separator is evaluated.
    a) If the block is contained in the separator, split the separator.
    b) If the block crosses with the separator, update the separator’s parameters.
    c) If the block covers the separator, remove the separator.
    '''

    def step2(self):
        pass

    '''
    Step 3
    Remove the four separators that stand at the border of the pool.
    '''

    def step3(self):
        pass

    def horizontalDetection(self, blocks):
        for block in blocks:
            temp = []
            for separator in temp:
                self.count += 1
                print(self.count)

                if SeparatorRule.horizontalRule1(block, separator):
                    y = block.y + block.height
                    separator_y = separator.y + separator.height
                    new_separator = SeparatorVO(0, y, self.width, separator_y, self.typ)

                    if new_separator != 0:
                        new_separator.one_side = block
                        self.separator_list.append(new_separator)

                    separator.height = block.y - separator.y
                    if separator.height == 0:
                        self.separator_list.remove(separator)
                    else:
                        separator.other_side(block)

                elif SeparatorRule.horizontalRule2(block, separator):
                    pass
                elif SeparatorRule.horizontalRule3(block, separator):
                    pass
                elif SeparatorRule.horizontalRule4(block, separator):
                    pass
                else:
                    pass

    def verticalDetection(self, blocks):
        for block in blocks:
            pass
