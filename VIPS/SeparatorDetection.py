# 4.2 Visual Separator Detection
# 4.2.1 Separator Detection

import sys
import time

from Rule.SeparatorRule import SeparatorRule


class SeparatorDetection:
    TYPE_HORIZONTAL = 'horizontal'
    TYPE_VERTICAL = 'vertical'

    x = 0  # Separator coordinate x
    y = 0  # Separator coordinate x
    width = 0   # Separator width
    height = 0  # Separator height
    count = 0
    weight = 7  # Separator weight

    separator_list = []

    typ = None
    top = None
    bottom = None

    def __init__(self, x, y, width, height, typ=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.typ = typ

    '''
    Execution function
    Identify the proper horizontal and vertical separator 
    @param blocks
    @param typ
    @return separator_list
    '''
    def runner(self, blocks, typ):
        self.typ = typ
        self.separator_list.clear()
        # Initialize Separator
        print('-------------------------------------Initialize Separator-------------------------------------')
        self.initializeSeparator()
        # Apply Rules
        print('-----------------------------------------Apply Rules------------------------------------------')
        self.applyRules(blocks)
        # Remove Separator
        print('---------------------------------------Remove Separator---------------------------------------')
        self.removeSeparator()
        return self.separator_list

    '''
    Step 1
    Initialize the separator list. The list starts with only one separator (Pbe, Pee) whose start pixel and end pixel 
    are corresponding to the borders of the pool.
    '''
    def initializeSeparator(self):
        separator = SeparatorDetection(0, 0, self.width, self.height, self.typ)
        self.separator_list.append(separator)

    '''
    Step 2
    For every block in the pool, the relation of the block with each separator is evaluated.
    a) If the block is contained in the separator, split the separator.
    b) If the block crosses with the separator, update the separator’s parameters.
    c) If the block covers the separator, remove the separator.
    @param blocks
    '''
    def applyRules(self, blocks):
        if SeparatorDetection.TYPE_HORIZONTAL == self.typ:
            self.horizontalDetection(blocks)
        elif SeparatorDetection.TYPE_VERTICAL == self.typ:
            self.verticalDetection(blocks)

    '''
    Step 3
    Remove the four separators that stand at the border of the pool.
    '''
    def removeSeparator(self):
        temp = []
        temp.extend(self.separator_list)
        for sep in temp:
            if self.typ == SeparatorDetection.TYPE_HORIZONTAL:
                if sep.x == 0 and (sep.y == 0 or sep.y + sep.height == self.height):
                    self.separator_list.remove(sep)
            else:
                if sep.y == 0 and (sep.x == 0 or sep.x + sep.width == self.width):
                    self.separator_list.remove(sep)

    '''
    Detect the horizontal separator based on the heuristic rules.
    @param blocks
    '''
    def horizontalDetection(self, blocks):
        for block in blocks:
            temp = []
            temp.extend(self.separator_list)
            for sep in temp:
                if SeparatorRule.horizontalRule1(block, sep):
                    # self.separator_list.remove(sep)
                    separator1_y = block.y + block.height
                    separator1_height_y = sep.height + sep.y
                    sep.height = separator1_height_y - separator1_y
                    new_separator = SeparatorDetection(0, separator1_y, self.width, sep.height, self.typ)
                    if new_separator != 0:
                        new_separator.top = block
                        self.separator_list.append(new_separator)

                    separator2_y = sep.y
                    separator2_height_y = block.y
                    sep.height = separator2_height_y - separator2_y
                    new_separator = SeparatorDetection(0, separator2_y, self.width, sep.height, self.typ)
                    if sep.height == 0:
                        self.separator_list.remove(sep)
                    else:
                        sep.bottom = block
                        self.separator_list.append(new_separator)

                elif SeparatorRule.horizontalRule2(block, sep):
                    separator_y = block.height + block.y
                    separator_height_y = sep.height + sep.y
                    sep.height = separator_height_y - separator_y

                    self.separator_list.remove(sep)
                    new_separator = SeparatorDetection(0, separator_y, self.width, sep.height, self.typ)
                    new_separator.top = block
                    self.separator_list.append(new_separator)

                elif SeparatorRule.horizontalRule3(block, sep):
                    sep.height = block.y - sep.y

                    self.separator_list.remove(sep)
                    new_separator = SeparatorDetection(0, sep.y, self.width, sep.height, self.typ)
                    new_separator.bottom = block
                    self.separator_list.append(new_separator)

                elif SeparatorRule.horizontalRule4(block, sep):
                    self.separator_list.remove(sep)

    '''
    Detect the vertical separator based on the heuristic rules.
    @param blocks
    '''
    def verticalDetection(self, blocks):
        self.separator_list.clear()
        for block1 in blocks:
            left_min_width = sys.maxsize
            left_x = 0
            left_y = 0
            left_width = 0
            left_height = 0

            right_min_width = sys.maxsize
            right_x = 0
            right_y = 0
            right_width = 0
            right_height = 0

            for block2 in blocks:
                if block1 == block2:
                    continue

                width_x1 = block1.x + block1.width
                width_x2 = block2.x + block2.width
                height_y1 = block1.y + block1.height
                height_y2 = block2.y + block2.height

                # Block 2 is on the left hand side of block 1
                if width_x2 < block1.x:
                    x = block2.x + block2.width  # width_x2
                    width = block1.x - x

                    sep = SeparatorDetection(0, 0, block1.x, block1.height, SeparatorDetection.TYPE_VERTICAL)
                    if SeparatorRule.verticalRule1(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block1.y
                            left_width = width
                            left_height = block1.height
                    elif SeparatorRule.verticalRule2(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block2.y
                            left_width = width
                            left_height = block2.height
                    elif SeparatorRule.verticalRule3(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block2.y
                            left_width = width
                            left_height = height_y1 - block2.y
                    elif SeparatorRule.verticalRule4(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block1.y
                            left_width = width
                            left_height = height_y2 - block1.y

                # Block 2 is on the right hand side of Block 1
                elif width_x1 < block2.x:
                    x = block1.x + block1.width  # width_x1
                    width = block2.x - x

                    sep = SeparatorDetection(x, block1.y, block1.width, block1.height, SeparatorDetection.TYPE_HORIZONTAL)
                    if SeparatorRule.verticalRule1(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = block1.height
                    elif SeparatorRule.verticalRule2(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block2.y
                            right_width = width
                            right_height = block2.height
                    elif SeparatorRule.verticalRule3(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = height_y1 - block2.height
                    elif SeparatorRule.verticalRule4(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = height_y2 - block1.height
            if left_min_width < sys.maxsize:
                separator = SeparatorDetection(left_x, left_y, left_width, left_height, SeparatorDetection.TYPE_VERTICAL)
                self.separator_list.append(separator)
            if right_min_width < sys.maxsize:
                separator = SeparatorDetection(right_x, right_y, right_width, right_height, SeparatorDetection.TYPE_VERTICAL)
                self.separator_list.append(separator)

    def __gt__(self, other):
        return self.weight > other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, type: {self.typ}'
